# -*- coding: utf-8 -*-
import os
import signal
import sys
import threading
import traceback
from abc import ABC
from typing import Dict, Any, Callable, Optional

import flask as flask
from pip_services4_commons.convert import JsonConverter
from pip_services4_commons.errors import UnknownException, BadRequestException, ErrorDescriptionFactory
from pip_services4_components.config import ConfigParams
from pip_services4_components.refer import DependencyResolver, IReferences, Descriptor
from pip_services4_container import Container
from pip_services4_data.validate import Schema
from pip_services4_observability.count import CompositeCounters
from pip_services4_observability.log import ConsoleLogger
from pip_services4_observability.trace import CompositeTracer
from pip_services4_rpc.trace import InstrumentTiming

from pip_services4_components.context import IContext, Context

from .CloudFunctionRequestHelper import CloudFunctionRequestHelper


class CloudFunction(Container, ABC):
    """
    Abstract Google Function, that acts as a container to instantiate and run components
    and expose them via external entry point.

    When handling calls "cmd" parameter determines which what action shall be called, while
    other parameters are passed to the action itself.

    Container configuration for this Google Function is stored in `"./config/config.yml"` file.
    But this path can be overriden by `CONFIG_PATH` environment variable.

    ### References ###
        - `*:logger:*:*:1.0`            (optional) :class:`ILogger <pip_services4_components.log.ILogger.ILogger>` components to pass log messages
        - `*:counters:*:*:1.0`        (optional) :class:`ICounters <pip_services4_components.count.ICounters.ICounters>` components to pass collected measurements
        - `*:service:cloudfunc:*:1.0`      (optional) :class:`ICounters <pip_services4_gcp.controller.iCloudFunctionservice.iCloudFunctionservice>` controller to handle action requests
        - `*:service:commandable-cloudfunc:*:1.0` (optional) :class:`ICounters <pip_services4_gcp.controller.iCloudFunctionservice.iCloudFunctionservice>` controller to handle action requests

    Example:

    .. code-block:: python
        class MyCloudFunction(CloudFunction):
            def __init__(self):
                super().__init__("mygroup", "MyGroup Google Function")


            cloud_function = MyCloudFunction()

            cloud_function.run()
            print("MyCloudFunction is started")

    """

    def __init__(self, name: str = None, description: str = None):
        """
        Creates a new instance of this Google Function function.

        :param name: (optional) a container name (accessible via ContextInfo)
        :param description: (optional) a container description (accessible via ContextInfo)
        """
        super(CloudFunction, self).__init__(name, description)

        self._logger = ConsoleLogger()

        # The performance counters.
        self._counters: CompositeCounters = CompositeCounters()
        # The tracer.
        self._tracer: CompositeTracer = CompositeTracer()
        # The dependency resolver.
        self._dependency_resolver: DependencyResolver = DependencyResolver()
        # The map of registered validation schemas.
        self._schemas: Dict[str, Schema] = {}
        # The map of registered actions.
        self._actions: Dict[str, Callable] = {}
        # The default path to config file.
        self._config_path: str = './config/config.yml'

    def __get_config_path(self) -> str:
        return os.environ.get('CONFIG_PATH') or self._config_path

    def __get_parameters(self) -> ConfigParams:
        return ConfigParams.from_value(os.environ)

    def __capture_errors(self, context: Optional[IContext]):
        def handle_exception(exc_type, exc_value, exc_traceback):
            self._logger.fatal(context, exc_value,
                               "Process is terminated")
            sys.exit(1)

        sys.excepthook = handle_exception

    def __capture_exit(self, context: Optional[IContext]):
        self._logger.info(
            context, "Press Control-C to stop the microservice...")

        # Activate graceful exit
        signal.signal(signal.SIGINT, lambda signum, frame: sys.exit())

        # Gracefully shutdown
        def shutdown(signum, frame):
            self.close(context)
            self._logger.info(context, 'Goodbye!' or sys.exit(0))
            sys.exit(0)

        signal.signal(signal.SIGTERM, shutdown)

    def set_references(self, references: IReferences):
        """
        Sets references to dependent components.

        :param references: references to locate the component dependencies.
        """
        super(CloudFunction, self).set_references(references)
        self._counters.set_references(references)
        self._dependency_resolver.set_references(references)

        self.register()

    def open(self, context: Optional[IContext]):
        """
        Opens the component.

        :param context: (optional) transaction id to trace execution through call chain.
        """
        if self.is_open():
            return

        super().open(context)
        self._register_services()

    def _instrument(self, context: Optional[IContext], name: str) -> InstrumentTiming:
        """
        Adds instrumentation to log calls and measure call time.
        It returns a InstrumentTiming object that is used to end the time measurement.

        Note: This method has been deprecated. Use CloudFunctionController instead.

        :param context: (optional) transaction id to trace execution through call chain.
        :param name: a method name.
        :return: object to end the time measurement.
        """
        self._logger.trace(context, "Executing %s method", name)
        self._counters.increment_one(name + ".exec_count")

        counter_timing = self._counters.begin_timing(name + ".exec_time")
        trace_timing = self._tracer.begin_trace(context, name, None)

        return InstrumentTiming(
            context, name, "exec",
            self._logger, self._counters, counter_timing, trace_timing
        )

    def run(self):
        """
        Runs this Azure Function, loads container configuration,
        instantiate components and manage their lifecycle,
        makes this function ready to access action calls.
        """
        ctx = Context.from_trace_id(self._info.name)

        path = self.__get_config_path()
        parameters = self.__get_parameters()
        self.read_config_from_file(ctx, path, parameters)

        # Note: signals works only in main thread
        if threading.current_thread().name == 'MainThread':
            self.__capture_exit(ctx)
            self.__capture_errors(ctx)

        self.open(ctx)

    def register(self):
        """
        Registers all actions in this Google Function.

        Note: Overloading of this method has been deprecated. Use CloudFunctionController instead.
        """

    def _register_services(self):
        """
        Registers all Google Function controller in the container.
        """
        # Extract regular and commandable Google Function controller from references
        services = self._references.get_optional(
            Descriptor("*", "controller", "cloudfunc", "*", "*"))
        cmd_services = self._references.get_optional(Descriptor(
            "*", "controller", "commandable-cloudfunc", "*", "*"))

        services.extend(cmd_services)

        # Register actions defined in those controller
        for service in services:
            # Check if the service implements required interface
            if not hasattr(service, 'get_actions'):
                continue
            actions = service.get_actions()
            for action in actions:
                self._register_action(action.cmd, action.schema, action.action)

    def _register_action(self, cmd: str, schema: Schema, action: Callable[[flask.Request], Any]):
        """
        Registers an action in this Google Function.

        Note: This method has been deprecated. Use CloudFunctionController instead.

        :param cmd: a action/command name.
        :param schema: a validation schema to validate received parameters.
        :param action: an action function that is called when action is invoked.
        """
        if not cmd:
            raise UnknownException(None, 'NO_COMMAND', 'Missing command')

        if not action:
            raise UnknownException(None, 'NO_ACTION', 'Missing action')

        if not callable(action):
            UnknownException(None, 'ACTION_NOT_FUNCTION',
                             'Action is not a function')

        if cmd in self._actions.keys():
            raise UnknownException(
                None, 'DUPLICATED_ACTION', f'"{cmd}" action already exists')

        # Hack!!! Wrapping action to preserve prototyping context
        def action_curl(req: flask.Request):
            # Perform validation
            if schema:
                params = req.args.to_dict()
                params.update({'body': req.json})

                trace_id = self._get_trace_id(req)
                err = schema.validate_and_return_exception(
                    trace_id, params, False)
                if err is not None:
                    return self._compose_error(err)
            # Todo: perform verification?
            return action(req)

        self._actions[cmd] = action_curl

    def _get_trace_id(self, req: flask.Request):
        """
        Returns traceId from Googel Function request.
        This method can be overloaded in child classes

        :param req: Googel Function request
        :return: Returns traceId from request
        """
        return CloudFunctionRequestHelper.get_trace_id(req)

    def _get_command(self, req: flask.Request):
        """
        Returns command from Google Function request.
        This method can be overloaded in child classes

        :param req: Google Function request
        :return: Returns command from request
        """
        return CloudFunctionRequestHelper.get_command(req)

    def _execute(self, req: flask.Request) -> Any:
        """
        Executes this Google Function and returns the result.
        This method can be overloaded in child classes
        if they need to change the default behavior

        :param req: the request to function
        :return: the result of the function execution (response)
        """
        cmd = self._get_command(req)
        trace_id = self._get_trace_id(req)
        if not cmd:
            return BadRequestException(
                trace_id,
                'NO_COMMAND',
                'Cmd parameter is missing'
            ).to_json()
        action = self._actions.get(cmd)
        if not action:
            return BadRequestException(
                trace_id,
                'NO_ACTION',
                'Action ' + cmd + ' was not found'
            ).with_details('command', cmd).to_json()

        return action(req)

    def __handler(self, req: flask.Request) -> Any:
        # If already started then execute
        if self.is_open():
            return self._execute(req)
        # Start before execute
        self.run()
        return self._execute(req)

    def get_handler(self) -> Callable[[flask.Request], Any]:
        """
        Gets entry point into this Google Function.

        :return: Return plugin function
        """
        return lambda req: self.__handler(req)

    def _compose_error(self, error: Exception) -> flask.Response:
        """
        Compose error serialized as ErrorDescription object and appropriate HTTP status code.
        If status code is not defined, it uses 500 status code.

        :param error: an error object to be sent.
        :return: HTTP response
        """
        basic_fillers = {'code': 'Undefined', 'status': 500, 'message': 'Unknown error',
                         'name': None, 'details': None,
                         'component': None, 'stack': None, 'cause': None}

        if error is None:
            error = type('error', (object,), basic_fillers)
        else:
            for k, v in basic_fillers.items():
                error.__dict__[k] = v if error.__dict__.get(
                    k) is None else error.__dict__[k]

        headers = {'Content-Type': 'application/json'}
        error = ErrorDescriptionFactory.create(error)
        error.stack_trace = traceback.format_exc()

        return flask.Response(JsonConverter.to_json(error), status=error.status, headers=headers)
