# -*- coding: utf-8 -*-
from pip_services4_gcp.containers import CloudFunction
from test.DummyFactory import DummyFactory


class DummyCloudFunction(CloudFunction):
    def __init__(self):
        super(DummyCloudFunction, self).__init__("dummy", "Dummy cloud function")
        self._factories.add(DummyFactory())
