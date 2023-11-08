# -*- coding: utf-8 -*-

import bottle
from pip_services4_components.refer import Descriptor, IReferences
from pip_services4_http.controller import RestController
from pip_services4_observability.count import CachedCounters

from pip_services4_prometheus.count.PrometheusCounterConverter import PrometheusCounterConverter


class PrometheusMetricsController(RestController):
    """
    Controller that exposes the **"/metrics"** and **"/metricsandreset"** routes for Prometheus to scap performance metrics.

    ### Configuration parameters ###
        - dependencies:
          - endpoint:              override for HTTP Endpoint dependency
          - prometheus-counters:   override for PrometheusCounters dependency
        - connection(s):
          - discovery_key:         (optional) a key to retrieve the connection from IDiscovery
          - protocol:              connection protocol: http or https
          - host:                  host name or IP address
          - port:                  port number
          - uri:                   resource URI or connection string with all parameters in it

    ### References ###
        - `*:logger:*:*:1.0`              (optional) :class:`ILogger <pip_services3_components.log.ILogger.ILogger>` components to pass log messages
        - `*:counters:*:*:1.0`            (optional) :class:`ICounters <pip_services3_components.count.ICounters.ICounters>` components to pass collected measurements
        - `*:discovery:*:*:1.0`           (optional) :class:`IDiscovery <pip_services3_components.connect.IDiscovery.IDiscovery>` controllers to resolve connection
        - `*:endpoint:http:*:1.0`         (optional) :class:`HttpEndpoint <pip_services3_rpc.controllers.HttpEndpoint.HttpEndpoint>` reference to expose REST operation
        - `*:counters:prometheus:*:1.0`   :class:`PrometheusCounters <pip_services4_prometheus.count.PrometheusCounters.PrometheusCounters>` reference to retrieve collected metrics

    See :class:`RestService <pip_services3_rpc.controllers.RestService.RestService>`, :class:`RestClient <pip_services3_rpc.clients.RestClient.RestClient>`

    Example:

    .. code-block:: python

        service = PrometheusMetricsController()
        service.configure(ConfigParams.from_tuples(
            "connection.protocol", "http",
            "connection.host", "localhost",
            "connection.port", 8080
        ))

        try:
            service.open(ctx)
            print("The Prometheus metrics service is accessible at http://+:8080/metrics")
        except Exception as err:
            # do something
    """

    def __init__(self):
        """
        Creates a new instance of this service.
        """
        super(PrometheusMetricsController, self).__init__()

        self.__cached_counters: CachedCounters = None
        self.__source: str = None
        self.__instance: str = None

        self._dependency_resolver.put("cached-counters", Descriptor("pip-services", "counters", "cached", "*", "1.0"))
        self._dependency_resolver.put("prometheus-counters",
                                      Descriptor("pip-services", "counters", "prometheus", "*", "1.0"))

    def set_references(self, references: IReferences):
        """
        Sets references to dependent components.

        :param references: references to locate the component dependencies.
        """
        super().set_references(references)

        self.__cached_counters = self._dependency_resolver.get_one_required('prometheus-counters')
        if self.__cached_counters is None:
            self.__cached_counters = self._dependency_resolver.get_one_required('cached-counters')

        context_info = references.get_one_optional(Descriptor("pip-services", "context-info", "default", "*", "1.0"))

        if context_info is not None and (self.__source == '' or self.__source is None):
            self.__source = context_info.name

        if context_info is not None and (self.__instance == '' or self.__instance is None):
            self.__instance = context_info.context_id

    def register(self):
        """
        Registers all service routes in HTTP endpoint.
        """
        self.register_route('get', 'metrics', None, self.__metrics)
        self.register_route('get', 'metricsandreset', None, self.__metrics_and_reset)

    def __metrics(self):
        """
        Handles metrics requests
        """
        counters = self.__cached_counters.get_all() if self.__cached_counters is not None else None
        body = PrometheusCounterConverter.to_string(counters, self.__source, self.__instance)

        bottle.response.set_header('content-type', 'text/plain')
        bottle.response.status = 200

        return body.encode('utf-8')

    def __metrics_and_reset(self):
        """
        Handles metricsandreset requests.
        The counters will be returned and then zeroed out.
        """
        counters = self.__cached_counters.get_all() if self.__cached_counters is not None else None
        body = PrometheusCounterConverter.to_string(counters, self.__source, self.__instance)

        if self.__cached_counters is not None:
            self.__cached_counters.clear_all()

        bottle.response.set_header('content-type', 'text/plain')
        bottle.response.status = 200

        return body.encode('utf-8')
