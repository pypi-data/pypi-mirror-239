# -*- coding: utf-8 -*-
from copy import deepcopy
from typing import Any, Dict, Optional

import requests
from pip_services4_commons.errors import ConnectionException, UnknownException, ErrorDescription, ErrorCategory, \
    ApplicationExceptionFactory
from pip_services4_components.config import IConfigurable, ConfigParams
from pip_services4_components.refer import IReferenceable, DependencyResolver, IReferences
from pip_services4_components.run import IOpenable
from pip_services4_observability.count import CompositeCounters
from pip_services4_observability.log import CompositeLogger
from pip_services4_observability.trace import CompositeTracer
from pip_services4_rpc.trace import InstrumentTiming

from pip_services4_components.context import IContext, ContextResolver

from requests.adapters import HTTPAdapter, Retry

from pip_services4_gcp.connect import GcpConnectionParams, GcpConnectionResolver


class CloudFunctionClient(IOpenable, IConfigurable, IReferenceable):
    """
    Abstract client that calls Google Functions.

    When making calls "cmd" parameter determines which what action shall be called, while
    other parameters are passed to the action itself.

    ### Configuration parameters ###
        - connections:
            - uri:           full connection uri with specific app and function name
            - protocol:      connection protocol
            - project_id:    is your Google Cloud Platform project ID
            - region:        is the region where your function is deployed
            - function:      is the name of the HTTP function you deployed
            - org_id:        organization name
        - options:
            - retries:               number of retries (default: 3)
            - connect_timeout:       connection timeout in milliseconds (default: 10 sec)
            - timeout:               invocation timeout in milliseconds (default: 10 sec)
        - credentials:
            - account: the service account name
            - auth_token:    Google-generated ID token or None if using custom auth (IAM)

    ### References ###
        - `*:logger:*:*:1.0`           (optional) :class:`ILogger <pip_services4_components.log.ILogger.ILogger>` components to pass log messages
        - `*:counters:*:*:1.0`         (optional) :class:`ICounters <pip_services4_components.count.ICounters.ICounters>` components to pass collected measurements
        - `*:discovery:*:*:1.0`         (optional) :class:`IDiscovery <pip_services4_components.connect.IDiscovery.IDiscovery>` controller to resolve connection
        - `*:credential-store:*:*:1.0`  (optional) Credential stores to resolve credentials

    See :class:`CloudFunction <pip_services4_gcp.containers.CloudFunction.CloudFunction>`,
    :class:`CommandableGoogleClient <pip_services4_gcp.clients.CommandableGoogleClient.CommandableGoogleClient>`

    Example:

    .. code-block:: python
        class MyCloudFunctionClient(CloudFunctionClient, IMyClient):
            def get_data(self, context, id) -> MyData:
                timing = self._instrument(context, 'myclient.get_data')
                result = self._call("get_data", context, {'id': id})

                data = MyData(**result)

                timing.end_timing()
                return data

        client = MyCloudFunctionClient()
        client.configure(ConfigParams.from_tuples(
            'connection.uri", "http://region-id.cloudfunctions.net/myfunction',
            'connection.protocol', 'http',
            'connection.region', 'region',
            'connection.function', 'myfunction',
            'connection.project_id', 'id',
            'credential.auth_token', 'XXX',
        ))

        result = client.get_data("123", "1")

    """

    def __init__(self):
        # The HTTP client.
        self._client: requests.Session = None

        # The Google Cloud connection parameters
        self._connection: GcpConnectionParams = None

        self._retries = 3

        # The default headers to be added to every request.
        self._headers: Dict[str, Any] = {}

        # The connection timeout in milliseconds.
        self._connect_timeout = 10000

        # The invocation timeout in milliseconds.
        self._timeout = 10000

        # The remote service uri which is calculated on open.
        self._uri: str = None

        # The dependencies resolver.
        self._dependency_resolver: DependencyResolver = DependencyResolver()

        # The connection resolver.
        self._connection_resolver: GcpConnectionResolver = GcpConnectionResolver()

        # The logger.
        self._logger: CompositeLogger = CompositeLogger()

        # The performance counters.
        self._counters: CompositeCounters = CompositeCounters()

        # The tracer.
        self._tracer: CompositeTracer = CompositeTracer()

    def configure(self, config: ConfigParams):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        self._connection_resolver.configure(config)
        self._dependency_resolver.configure(config)

        self._connect_timeout = config.get_as_integer_with_default('options.connect_timeout', self._connect_timeout)
        self._retries = config.get_as_integer_with_default("options.retries", self._retries)
        self._timeout = config.get_as_integer_with_default("options.timeout", self._timeout)

    def set_references(self, references: IReferences):
        """
        Sets references to dependent components.

        :param references: references to locate the component dependencies.
        """
        self._logger.set_references(references)
        self._counters.set_references(references)
        self._connection_resolver.set_references(references)
        self._dependency_resolver.set_references(references)

    def _instrument(self, context: Optional[IContext], name: str) -> InstrumentTiming:
        """
        Adds instrumentation to log calls and measure call time.
        It returns a CounterTiming object that is used to end the time measurement.

        :param context: (optional) transaction id to trace execution through call chain.
        :param name: a method name.
        :return: object to end the time measurement.
        """
        self._logger.trace(context, "Executing %s method", name)
        self._counters.increment_one(name + ".exec_count")

        counter_timing = self._counters.begin_timing(name + ".exec_time")
        trace_timing = self._tracer.begin_trace(context, name, None)
        return InstrumentTiming(context, name, 'exec',
                                self._logger, self._counters, counter_timing, trace_timing)

    def is_open(self) -> bool:
        """
        Checks if the component is opened.

        :return: true if the component has been opened and false otherwise.
        """
        return self._client is not None

    def open(self, context: Optional[IContext]):
        """
        Opens the component.

        :param context: (optional) transaction id to trace execution through call chain.
        """
        self._connection = self._connection_resolver.resolve(context)

        if self._connection.get_auth_token() is not None:
            self._headers['Authorization'] = 'bearer ' + self._connection.get_auth_token()

        try:
            self._uri = self._connection.get_uri()

            self._client = requests.Session()
            self._client.headers.update(self._headers)

            adapter = HTTPAdapter(max_retries=Retry(
                total=self._retries,
                backoff_factor=self._timeout / 1000,
            ))

            self._client.mount("https://", adapter)
            self._client.mount("http://", adapter)
            self._client.params = {
                'url': self._uri,
                'timeout': (self._connect_timeout / 1000, self._timeout / 1000),
            }

            self._logger.debug(context, "Google function client connected to %s",
                               self._connection.get_uri())

        except Exception as ex:
            self._client = None

            raise ConnectionException(
                context, "CANNOT_CONNECT", "Connection to Google function service failed"
            ).wrap(ex).with_details("url", self._uri)

    def close(self, context: Optional[IContext]):
        """
        Closes component and frees used resources.

        :param context: (optional) transaction id to trace execution through call chain.
        """
        if self.is_open():
            return

        if self._client is not None:
            # Eat exceptions
            try:
                self._logger.debug(context, "Closed Google function service at %s", self._uri)
            except Exception as ex:
                self._logger.warn(context, "Failed while closing Google function service: %s", ex)

            self._client = None
            self._uri = None

    def _invoke(self, cmd: str, context: Optional[IContext], args: dict = None) -> Optional[dict]:
        if not cmd:
            raise UnknownException(None, 'NO_COMMAND', 'Cmd parameter is missing')

        args = deepcopy(args or {})
        args['cmd'] = cmd
        args['trace_id'] = ContextResolver.get_trace_id(context)

        response = self._client.post(self._uri, json=args)

        # Handling 204 codes
        if response.status_code == 204:
            return

        data = None if not response.content else response.json()

        # Restore application exception
        if response.status_code >= 400:
            if data:
                data = ErrorDescription.from_json(data)
            else:
                data = ErrorDescription()
                data.code = response.status_code
                data.message = response.reason
                data.category = ErrorCategory.Unknown
            raise ApplicationExceptionFactory.create(data).with_cause(Exception(response.text))

        return data

    def _call(self, cmd: str, context: Optional[IContext], params: dict = None) -> Optional[dict]:
        """
        Calls a Google Function action.

        :param cmd: an action name to be called.
        :param context: (optional) transaction id to trace execution through call chain.
        :param params: (optional) action parameters.
        :return: action result.
        """
        return self._invoke(cmd, context, params)
