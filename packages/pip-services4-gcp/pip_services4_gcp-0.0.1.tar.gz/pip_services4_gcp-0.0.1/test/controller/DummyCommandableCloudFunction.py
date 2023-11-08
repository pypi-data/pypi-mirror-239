# -*- coding: utf-8 -*-
from pip_services4_components.refer import Descriptor

from pip_services4_gcp.containers import CommandableCloudFunction
from ..DummyFactory import DummyFactory


class DummyCommandableCloudFunction(CommandableCloudFunction):
    def __init__(self):
        super(DummyCommandableCloudFunction, self).__init__("dummy", "Dummy commandable cloud function")
        self._dependency_resolver.put('service',
                                      Descriptor('pip-services', 'service', 'default', '*', '*'))
        self._factories.add(DummyFactory())
