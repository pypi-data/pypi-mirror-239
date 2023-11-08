# -*- coding: utf-8 -*-
from pip_services4_components.refer import Descriptor

from pip_services4_gcp.controller import CommandableCloudFunctionController


class DummyCommandableCloudFunctionController(CommandableCloudFunctionController):
    def __init__(self):
        super(DummyCommandableCloudFunctionController, self).__init__('dummies')
        self._dependency_resolver.put('service', Descriptor('pip-services', 'service', 'default', '*', '*'))