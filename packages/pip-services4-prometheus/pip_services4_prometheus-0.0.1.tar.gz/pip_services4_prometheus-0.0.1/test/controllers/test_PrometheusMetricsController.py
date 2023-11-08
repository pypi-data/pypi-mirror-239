# -*- coding: utf-8 -*-
from pip_services4_components.config import ConfigParams
from pip_services4_components.context import ContextInfo
from pip_services4_components.refer import Descriptor, References
from pip_services4_observability.count import CounterType
from urllib3 import HTTPConnectionPool

from pip_services4_prometheus.count.PrometheusCounters import PrometheusCounters
from pip_services4_prometheus.controllers.PrometheusMetricsController import PrometheusMetricsController

rest_config = ConfigParams.from_tuples(
    "connection.protocol", "http",
    "connection.host", "localhost",
    "connection.port", 3000,
)


class TestPrometheusMetricsController:
    service: PrometheusMetricsController
    counters: PrometheusCounters
    rest = None

    @classmethod
    def setup_class(cls):
        cls.service = PrometheusMetricsController()
        cls.counters = PrometheusCounters()
        rest_config.append({})
        cls.service.configure(rest_config)

        context_info = ContextInfo()
        context_info.name = 'Test'
        context_info.description = 'This is a test container'

        references = References.from_tuples(
            Descriptor("pip-services", "context-info", "default", "default", "1.0"), context_info,
            Descriptor("pip-services", "counters", "prometheus", "default", "1.0"), cls.counters,
            Descriptor("pip-services", "metrics-controller", "prometheus", "default", "1.0"), cls.service
        )

        cls.counters.set_references(references)
        cls.service.set_references(references)

        cls.counters.open(None)
        cls.service.open(None)

    @classmethod
    def teardown_class(cls):
        cls.service.close(None)
        cls.counters.close(None)

    def setup_method(self, method=None):
        url = 'http://localhost:3000'
        self.rest = HTTPConnectionPool(url.split('://')[-1])

    def test_metrics(self):
        self.counters.increment_one('test.counter1')
        self.counters.stats('test.counter2', 2)
        self.counters.last('test.counter3', 3)
        self.counters.timestamp_now('test.counter4')

        response = self.rest.request('GET', '/metrics')
        assert response is not None
        assert response.status < 400
        assert len(response.data.decode('utf-8')) > 0

    def test_metrics_and_reset(self):
        self.counters.increment_one('test.counter1')
        self.counters.stats('test.counter2', 2)
        self.counters.last('test.counter3', 3)
        self.counters.timestamp_now('test.counter4')

        response = self.rest.request('GET', '/metricsandreset')
        assert response is not None
        assert response.status < 400
        assert len(response.data.decode('utf-8')) > 0

        counter1 = self.counters.get("test.counter1", CounterType.Increment)
        counter2 = self.counters.get("test.counter2", CounterType.Statistics)
        counter3 = self.counters.get("test.counter3", CounterType.LastValue)
        counter4 = self.counters.get("test.counter4", CounterType.Timestamp)

        assert counter1.count is None
        assert counter2.count is None
        assert counter3.last is None
        assert counter4.time is None
