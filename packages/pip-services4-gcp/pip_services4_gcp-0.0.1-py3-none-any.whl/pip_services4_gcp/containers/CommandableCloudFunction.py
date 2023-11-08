# -*- coding: utf-8 -*-
import json
from typing import Union, Any

import flask
from pip_services4_commons.convert import JsonConverter

from pip_services4_components.exec import Parameters
from pip_services4_data.query import DataPage
from pip_services4_rpc.commands import CommandSet, ICommandable

from pip_services4_components.context import Context

from .CloudFunction import CloudFunction
from .CloudFunctionRequestHelper import CloudFunctionRequestHelper


class CommandableCloudFunction(CloudFunction):
    """
    Abstract Google Function function, that acts as a container to instantiate and run components
    and expose them via external entry point. All actions are automatically generated for commands
    defined in :class:`ICommandable <pip_services4_commons.commands.ICommandable.ICommandable>` components.
    Each command is exposed as an action defined by "cmd" parameter.

    Container configuration for this Google Function is stored in `"./config/config.yml"` file.
    But this path can be overridden by `CONFIG_PATH` environment variable.

    Note: This component has been deprecated. Use CloudFunctionController instead.

    ### References ###
        - `*:logger:*:*:1.0`            (optional) :class:`ILogger <pip_services4_components.log.ILogger.ILogger>` components to pass log messages
        - `*:counters:*:*:1.0`        (optional) :class:`ICounters <pip_services4_components.count.ICounters.ICounters>` components to pass collected measurements
        - `*:service:cloudfunc:*:1.0`      (optional) :class:`ICounters <pip_services4_gcp.controller.iCloudFunctionservice.iCloudFunctionservice>` controller to handle action requests
        - `*:service:commandable-cloudfunc:*:1.0` (optional) :class:`ICounters <pip_services4_gcp.controller.iCloudFunctionservice.iCloudFunctionservice>` controller to handle action requests

    Example:

    .. code-block:: python
        class MyCloudFunction(CommandableCloudFunction):
            def __init__(self):
                super().__init__("mygroup", "MyGroup CloudFunction")
                self.__dependency_resolver.put("service", Descriptor("mygroup","service","*","*","1.0"))


        cloud_function = MyCloudFunction()
        service.run()
        print("MyCloudFunction is started")

    """

    def __init__(self, name: str = None, description: str = None):
        """
        Creates a new instance of this Google Function.

        :param name: (optional) a container name (accessible via ContextInfo)
        :param description: (optional) a container description (accessible via ContextInfo)
        """
        super(CommandableCloudFunction, self).__init__(name, description)

    def _get_parameters(self, req: flask.Request) -> Parameters:
        """
        Returns body from Google Function request.
        This method can be overloaded in child classes

        :param req: Googl Function request
        :return: Returns Parameters from request
        """
        return CloudFunctionRequestHelper.get_parameters(req)

    def __register_command_set(self, command_set: CommandSet):
        commands = command_set.get_commands()
        for i in range(len(commands)):
            command = commands[i]

            def wrapper(command):
                # wrapper for passing context
                def action(req: flask.Request):
                    ctx = Context.from_trace_id(self._get_trace_id(req))
                    args = self._get_parameters(req)
                    timing = self._instrument(ctx, self._info.name + '.' + command.get_name())

                    try:
                        result = command.execute(ctx, args)
                        # Conversion to response data format
                        result = self.__to_response_format(result)
                        return result
                    except Exception as e:
                        timing.end_failure(e)
                        return self._compose_error(e)
                    finally:
                        timing.end_timing()

                return action

            self._register_action(command.get_name(), None, wrapper(command))

    def register(self):
        """
        Registers all actions in this Google Function.
        """
        service: ICommandable = self._dependency_resolver.get_one_required('service')
        command_set = service.get_command_set()
        self.__register_command_set(command_set)

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
