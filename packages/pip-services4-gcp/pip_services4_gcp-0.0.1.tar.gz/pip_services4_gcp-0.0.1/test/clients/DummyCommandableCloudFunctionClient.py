# -*- coding: utf-8 -*-
from typing import Optional

from pip_services4_data.query import FilterParams, PagingParams, DataPage

from pip_services4_components.context import IContext

from pip_services4_gcp.clients.CommandableCloudFunctionClient import CommandableCloudFunctionClient
from test.Dummy import Dummy
from test.IDummyClient import IDummyClient


class DummyCommandableCloudFunctionClient(CommandableCloudFunctionClient, IDummyClient):
    def __init__(self):
        super(DummyCommandableCloudFunctionClient, self).__init__('dummies')

    def get_dummies(self, context: Optional[IContext], filter_params: FilterParams, paging: PagingParams) -> DataPage:
        response = self.call_command('dummies.get_dummies', context, {
            'filter': filter_params,
            'paging': paging.to_json()
        })

        page = DataPage([], response.get('total'))

        if response.get('data'):
            for item in response['data']:
                page.data.append(Dummy(**item))

        return page

    def get_dummy_by_id(self, context: Optional[IContext], dummy_id: str) -> Optional[Dummy]:
        response = self.call_command('dummies.get_dummy_by_id', context, {'dummy_id': dummy_id})

        if response is None or len(response.keys()) == 0:
            return None

        return Dummy(**response)

    def create_dummy(self, context: Optional[IContext], dummy: Dummy) -> Dummy:
        response = self.call_command('dummies.create_dummy', context, {'dummy': dummy.to_dict()})

        if response:
            return Dummy(**response)

    def update_dummy(self, context: Optional[IContext], dummy: Dummy) -> Dummy:
        response = self.call_command('dummies.update_dummy', context, {'dummy': dummy.to_dict()})

        if response:
            return Dummy(**response)

    def delete_dummy(self, context: Optional[IContext], dummy_id: str) -> Dummy:
        response = self.call_command('dummies.delete_dummy', context, {'dummy_id': dummy_id})

        if response:
            return Dummy(**response)
