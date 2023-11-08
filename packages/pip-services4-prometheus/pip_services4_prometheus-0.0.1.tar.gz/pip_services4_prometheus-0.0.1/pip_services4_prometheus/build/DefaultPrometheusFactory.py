# -*- coding: utf-8 -*-
from pip_services4_components.build import Factory
from pip_services4_components.refer import Descriptor

from pip_services4_prometheus.count.PrometheusCounters import PrometheusCounters
from pip_services4_prometheus.controllers.PrometheusMetricsController import PrometheusMetricsController


class DefaultPrometheusFactory(Factory):
    """
    Creates Prometheus components by their descriptors.

    See :class:`Factory <pip_services3_components.build.Factory.Factory>`,
    :class:`PrometheusCounters <pip_services4_prometheus.count.PrometheusCounters.PrometheusCounters>`,
    :class:`PrometheusMetricsController <pip_services4_prometheus.controllers.PrometheusMetricsController.PrometheusMetricsController>`
    """
    PrometheusCountersDescriptor = Descriptor("pip-services", "counters", "prometheus", "*", "1.0")
    PrometheusMetricsControllerDescriptor = Descriptor("pip-services", "metrics-controller", "prometheus", "*", "1.0")

    def __init__(self):
        """
        Create a new instance of the factory.
        """
        super(DefaultPrometheusFactory, self).__init__()
        self.register_as_type(DefaultPrometheusFactory.PrometheusCountersDescriptor, PrometheusCounters)
        self.register_as_type(DefaultPrometheusFactory.PrometheusMetricsControllerDescriptor, PrometheusMetricsController)
