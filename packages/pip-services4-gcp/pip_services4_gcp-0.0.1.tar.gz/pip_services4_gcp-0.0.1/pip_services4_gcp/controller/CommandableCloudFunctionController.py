# -*- coding: utf-8 -*-
import json
import flask

from typing import Any, Union

from pip_services4_commons.convert import JsonConverter
from pip_services4_data.query import DataPage
from pip_services4_rpc.commands import CommandSet, ICommandable
from pip_services4_components.exec import Parameters

from pip_services4_components.context import Context

from pip_services4_gcp.containers import CloudFunctionRequestHelper
from pip_services4_gcp.controller import CloudFunctionController


class CommandableCloudFunctionController(CloudFunctionController):
    """
    Abstract controller that receives commands via Google Function protocol
    to operations automatically generated for commands defined in :class:`ICommandable <pip_services4_commons.commands.ICommandable.ICommandable>`.
    Each command is exposed as invoke method that receives command name and parameters.

    Commandable controller require only 3 lines of code to implement a robust external
    Google Function-based remote interface.

    This service is intended to work inside Google Function container that
    exploses registered actions externally.

    ### Configuration parameters ###
        - dependencies:
            - service:            override for Service dependency

    ### References ###
        - `*:logger:*:*:1.0`           (optional) :class:`ILogger <pip_services4_components.log.ILogger.ILogger>` components to pass log messages
        - `*:counters:*:*:1.0`         (optional) :class:`ICounters <pip_services4_components.count.ICounters.ICounters>` components to pass collected measurements

    Example:

    .. code-block:: python

            class MyCommandableCloudFunctionController(CommandableCloudFunctionController):
                def __init__(self):
                    super().__init__("mydata")
                    self._dependency_resolver.put(
                        "service",
                        Descriptor("mygroup","service","*","*","1.0")
                  )

            controller = MyCommandableCloudFunctionService()
            controller.set_references(References.from_tuples(
                Descriptor("mygroup","service","default","default","1.0"), service
            ))

            controller.open("123")
            print("The Google Function controller is running")

    """

    def __init__(self, name: str):
        """
        Creates a new instance of the service.

        :param name: a service name.
        """
        super().__init__(name)
        self._dependency_resolver.put('service', 'none')

        self.__command_set: CommandSet = None

    def _get_parameters(self, req: flask.Request) -> Parameters:
        """
        Returns body from Google Function request.
        This method can be overloaded in child classes

        :param req: Google Function request
        :return: Parameters from request
        """
        return CloudFunctionRequestHelper.get_parameters(req)

    def register(self):
        """
        Registers all actions in Google Function.
        """

        def wrapper(command):
            # wrapper for passing context
            def action(req: flask.Request):
                trace_id = self._get_trace_id(req)

                args = Parameters.from_value({} if not req.is_json else req.get_json())
                if trace_id:
                    args.remove('trace_id')
                ctx = Context.from_trace_id(trace_id)
                timing = self._instrument(ctx, name)
                try:
                    result = command.execute(ctx, args)
                    # Conversion to response data format
                    result = self.__to_response_format(result)
                    timing.end_timing()
                    return result
                except Exception as e:
                    timing.end_failure(e)
                    return self._compose_error(e)

            return action

        service: ICommandable = self._dependency_resolver.get_one_required('service')
        self.__command_set = service.get_command_set()

        commands = self.__command_set.get_commands()
        for index in range(len(commands)):
            command = commands[index]
            name = command.get_name()

            self._register_action(name, None, wrapper(command))

    def __to_response_format(self, res: Any) -> Union[dict, tuple]:
        if res is None:
            return '', 204
        if not isinstance(res, (int, str, dict, tuple, list, bytes, float, flask.Response)):
            if hasattr(res, 'to_dict'):
                res = res.to_dict()
            elif hasattr(res, 'to_json'):
                if isinstance(res, DataPage) and len(res.data) > 0 and not isinstance(res.data[0], dict):
                    res.data = json.loads(JsonConverter.to_json(res.data))
                res = res.to_json()
            else:
                res = JsonConverter.to_json(res)

        return res
