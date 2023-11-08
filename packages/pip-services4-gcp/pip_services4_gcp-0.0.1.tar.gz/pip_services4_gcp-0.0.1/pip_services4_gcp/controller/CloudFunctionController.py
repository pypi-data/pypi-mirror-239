# -*- coding: utf-8 -*-
import re
import traceback
from abc import abstractmethod
from typing import List, Optional, Callable, Any

import flask
from pip_services4_commons.convert import JsonConverter
from pip_services4_commons.errors import ErrorDescriptionFactory
from pip_services4_components.config import IConfigurable, ConfigParams
from pip_services4_components.refer import IReferenceable, DependencyResolver, IReferences
from pip_services4_components.run import IOpenable
from pip_services4_data.validate import Schema
from pip_services4_observability.count import CompositeCounters
from pip_services4_observability.log import CompositeLogger
from pip_services4_observability.trace import CompositeTracer
from pip_services4_rpc.trace import InstrumentTiming

from pip_services4_components.context import IContext

from .CloudFunctionAction import CloudFunctionAction
from .ICloudFunctionController import ICloudFunctionController
from ..containers.CloudFunctionRequestHelper import CloudFunctionRequestHelper


class CloudFunctionController(ICloudFunctionController, IOpenable, IConfigurable, IReferenceable):
    """
    Abstract controller that receives remove calls via Google Function protocol.

    This service is intended to work inside CloudFunction container that
    exposes registered actions externally.

    ### Configuration parameters ###
        - dependencies:
            - service:            override for Service dependency

    ### References ###
        - `*:logger:*:*:1.0`           (optional) :class:`ILogger <pip_services4_components.log.ILogger.ILogger>` components to pass log messages
        - `*:counters:*:*:1.0`         (optional) :class:`ICounters <pip_services4_components.count.ICounters.ICounters>` components to pass collected measurements

    Example:

    .. code-block:: python

        class MyCloudFunctionController(CloudFunctionController):
             _service: IMyService
           ...

           def __init__(self):
                super().__init__('v1.mycontroller')
                self._dependency_resolver.put(
                    "service",
                    Descriptor("mygroup","service","*","*","1.0")
                )

           def set_references(self, references: IReferences):
              super().set_references(references)
              self._service = self._dependency_resolver.get_required("service")


           def __action(self, req):
                trace_id = self._get_trace_id(req)
                id = req.args.get('id')
                return self._service.get_my_data(trace_id, id)

           def register(self):
               self.register_action("get_my_data", None, __action)

               ...


        controller = MyCloudFunctionController()
        controller.configure(ConfigParams.from_tuples(
            "connection.protocol", "http",
            "connection.host", "localhost",
            "connection.port", 8080
        ))

        controller.set_references(References.from_tuples(
            Descriptor("mygroup","service","default","default","1.0"), service
        ))

        controller.open("123")

    """

    def __init__(self, name: str):
        """
        Creates an instance of this service.

        :param name: a service name to generate action cmd.
        """
        self.__name: str = name
        self.__actions: List[CloudFunctionAction] = []
        self.__interceptors: List[Callable[[flask.Request, Callable[[flask.Request], Any]], Any]] = []
        self.__opened: bool = False

        # The dependency resolver.
        self._dependency_resolver: DependencyResolver = DependencyResolver()

        # The logger.
        self._logger: CompositeLogger = CompositeLogger()

        # The performance counters.
        self._counters: CompositeCounters = CompositeCounters()

        # The tracer.
        self._tracer: CompositeTracer = CompositeTracer()

    def configure(self, config: ConfigParams):
        """
        Configures object by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        self._dependency_resolver.configure(config)

    def set_references(self, references: IReferences):
        """
        Sets references to dependent components.

        :param references: references to locate the component dependencies.
        """
        self._logger.set_references(references)
        self._counters.set_references(references)
        self._tracer.set_references(references)
        self._dependency_resolver.set_references(references)

    def get_actions(self) -> List[CloudFunctionAction]:
        """
        Get all actions supported by the service.

        :return: an array with supported actions.
        """
        return self.__actions

    def _instrument(self, context: Optional[IContext], name: str) -> InstrumentTiming:
        """
        Adds instrumentation to log calls and measure call time.
        It returns a Timing object that is used to end the time measurement.

        :param context: (optional) transaction id to trace execution through call chain.
        :param name: a method name.
        :return: Timing object to end the time measurement.
        """
        self._logger.trace(context, "Executing %s method", name)
        self._counters.increment_one(name + ".exec_count")

        counter_timing = self._counters.begin_timing(name + ".exec_time")
        trace_timing = self._tracer.begin_trace(context, name, None)

        return InstrumentTiming(context, name, "exec",
                                self._logger, self._counters, counter_timing, trace_timing)

    def is_open(self) -> bool:
        """
        Checks if the component is opened.

        :return: true if the component has been opened and false otherwise.
        """
        return self.__opened

    def open(self, context: Optional[IContext]):
        """
        Opens the component.

        :param context: (optional) transaction id to trace execution through call chain.
        """
        if self.__opened:
            return

        self.register()

        self.__opened = True

    def close(self, context: Optional[IContext]):
        """
        Closes component and frees used resources.

        :param context: (optional) transaction id to trace execution through call chain.
        """
        if not self.__opened:
            return

        self.__opened = False
        self.__actions = []
        self.__interceptors = []

    def _apply_validation(self, schema: Schema, action: Callable[[flask.Request], Any]) -> Callable[
        [flask.Request], Any]:
        # Create an action function

        def action_wrapper(req: flask.Request):
            # Validate object
            if schema and req:
                params = req.args.to_dict()
                params.update({'body': req.json})

                # Perform validation
                trace_id = self._get_trace_id(req)
                err = schema.validate_and_return_exception(
                    trace_id, params, False)
                if err is not None:
                    return self._compose_error(err)

            return action(req)

        return action_wrapper

    def _apply_interceptors(self, action: Callable[[flask.Request], Any]) -> Callable[[flask.Request], Any]:
        action_wrapper = action

        index = len(self.__interceptors) - 1
        while index >= 0:
            interceptor = self.__interceptors[index]

            def action_wrapper(action): return lambda params: interceptor(
                params, action)(action_wrapper)

        return action_wrapper

    def _generate_action_cmd(self, name: str) -> str:
        cmd = name
        if self.__name is not None:
            cmd = self.__name + '.' + cmd

        return cmd

    def _register_action(self, name: str, schema: Schema, action: Callable[[flask.Request], Any]):
        """
        Registers a action in Google Function function.

        :param name: an action name
        :param schema: a validation schema to validate received parameters.
        :param action: an action function that is called when operation is invoked.
        """
        action_wrapper = self._apply_validation(schema, action)
        action_wrapper = self._apply_interceptors(action_wrapper)

        register_action: CloudFunctionAction = CloudFunctionAction(self._generate_action_cmd(name), schema,
                                                                   lambda req: action_wrapper(req))

        self.__actions.append(register_action)

    def _register_action_with_auth(self, name: str, schema: Schema,
                                   authorize: Callable[[Any, Callable[[Any], Any]], Any], action: Callable[[Any], Any]):
        """
        Registers an action with authorization.

        :param name: an action name
        :param schema: a validation schema to validate received parameters.
        :param authorize: an authorization interceptor
        :param action: an action function that is called when operation is invoked.
        """
        action_wrapper = self._apply_validation(schema, action)

        # Add authorization just before validation
        action_wrapper = lambda req: authorize(req, action_wrapper)

        action_wrapper = self._apply_interceptors(action_wrapper)

        register_action: CloudFunctionAction = CloudFunctionAction(self._generate_action_cmd(name), schema,
                                                                   lambda req: action_wrapper(req))

        self.__actions.append(register_action)

    def _register_interceptor(self, cmd: str, action: Callable[[flask.Request], Any]):
        """
        Registers a middleware for actions in Google Function service.

        :param cmd: the command name for intercept or regex.
        :param action: an action function that is called when middleware is invoked.
        """

        def intercept_wrapper(req: flask.Request, next: Callable[[flask.Request], Any]) -> Any:
            currCmd = self._get_command(req)
            match = re.match('.*' + cmd, currCmd) is not None
            if cmd is not None and cmd != '' and not match:
                return next(req)
            else:
                return action(req)

        self.__interceptors.append(intercept_wrapper)

    @abstractmethod
    def register(self):
        """
        Registers all service routes in HTTP endpoint.
        This method is called by the service and must be overriden
        in child classes.
        """

    def _get_trace_id(self, req: flask.Request):
        """
        Returns traceId from Google Function request.
        This method can be overloaded in child classes

        :param req: the function request
        :return: returns traceId from request
        """
        return CloudFunctionRequestHelper.get_trace_id(req)

    def _get_command(self, req: flask.Request) -> str:
        """
        Returns command from Google Function request.
        This method can be overloaded in child classes

        :param req: the function request
        :return: returns command from request
        """
        return CloudFunctionRequestHelper.get_command(req)

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
