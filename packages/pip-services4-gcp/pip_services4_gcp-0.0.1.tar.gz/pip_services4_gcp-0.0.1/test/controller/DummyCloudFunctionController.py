# -*- coding: utf-8 -*-
import flask
from pip_services4_commons.convert import TypeCode
from pip_services4_components.refer import Descriptor, IReferences
from pip_services4_data.query import FilterParams, PagingParams
from pip_services4_data.validate import ObjectSchema, FilterParamsSchema, PagingParamsSchema

from pip_services4_gcp.controller import CloudFunctionController
from ..Dummy import Dummy
from ..DummySchema import DummySchema
from ..IDummyService import IDummyService


class DummyCloudFunctionController(CloudFunctionController):
    def __init__(self):
        super(DummyCloudFunctionController, self).__init__('dummies')
        self._dependency_resolver.put('service',
                                      Descriptor('pip-services', 'service', 'default', '*', '*'))

        self._service: IDummyService = None
        self._headers = {
            'Content-Type': 'application/json'
        }

    def set_references(self, references: IReferences):
        super(DummyCloudFunctionController, self).set_references(references)
        self._service = self._dependency_resolver.get_one_required('service')

    def __get_page_by_filter(self, req: flask.Request):
        params = req.get_json()

        page = self._service.get_page_by_filter(
            self._get_trace_id(req),
            FilterParams(params.get('filter', {})),
            PagingParams.from_value(params.get("paging"))
        )

        if len(page.data) > 0:
            serealized_items = []
            for item in page.data:
                serealized_items.append(item.to_dict())

            page = page.to_json()
            page['data'] = serealized_items

        return page, self._headers

    def __get_one_by_id(self, req: flask.Request):
        params = req.get_json()

        dummy = self._service.get_one_by_id(
            self._get_trace_id(req),
            params.get('dummy_id')
        )

        if dummy:
            return dummy.to_dict(), self._headers
        else:
            return '', 204

    def __create(self, req: flask.Request):
        params = req.get_json()

        dummy = self._service.create(
            self._get_trace_id(req),
            Dummy(**params.get('dummy'))
        )

        return dummy.to_dict(), self._headers

    def __update(self, req: flask.Request):
        params = req.get_json()

        dummy = self._service.update(
            self._get_trace_id(req),
            Dummy(**params.get('dummy'))
        )

        return dummy.to_dict(), self._headers

    def __delete_by_id(self, req: flask.Request):
        params = req.get_json()

        dummy = self._service.delete_by_id(
            self._get_trace_id(req),
            params.get('dummy_id')
        )

        if dummy:
            return dummy.to_dict(), self._headers
        else:
            return '', 204

    def register(self):
        self._register_action(
            'get_dummies',
            ObjectSchema(True)
                .with_optional_property('body',
                                        ObjectSchema(True)
                                        .with_optional_property('filter', FilterParamsSchema())
                                        .with_optional_property('paging', PagingParamsSchema())),
            self.__get_page_by_filter
        )

        self._register_action(
            'get_dummy_by_id',
            ObjectSchema(True)
                .with_optional_property('body',
                                        ObjectSchema(True)
                                        .with_optional_property('dummy_id', TypeCode.String)),
            self.__get_one_by_id
        )

        self._register_action(
            'create_dummy',
            ObjectSchema(True)
                .with_optional_property('body',
                                        ObjectSchema(True)
                                        .with_required_property('dummy', DummySchema())),
            self.__create
        )

        self._register_action(
            'update_dummy',
            ObjectSchema(True)
                .with_optional_property('body',
                                        ObjectSchema(True)
                                        .with_required_property('dummy', DummySchema())),
            self.__update
        )

        self._register_action(
            'delete_dummy',
            ObjectSchema(True)
                .with_optional_property('body',
                                        ObjectSchema(True)
                                        .with_required_property('dummy_id', TypeCode.String)),
            self.__delete_by_id
        )
