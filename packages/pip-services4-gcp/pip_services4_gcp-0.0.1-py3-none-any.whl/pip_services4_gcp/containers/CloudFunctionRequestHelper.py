# -*- coding: utf-8 -*-
import flask

from pip_services4_components.exec import Parameters


class CloudFunctionRequestHelper:
    """
    Class that helps to prepare function requests
    """

    @staticmethod
    def get_trace_id(req: flask.Request) -> str:
        """
        Returns traceId from Google Function request.

        :param req: the Google Function request
        :return: returns traceId from request
        """
        trace_id = req.view_args.get('trace_id', '')
        try:
            if trace_id == '' and req.is_json:
                trace_id = req.json.get('trace_id', '')
                if trace_id == '':
                    trace_id = req.args.get('trace_id', '')
        except Exception as e:
            # Ignore the error
            pass

        return trace_id

    @staticmethod
    def get_command(req: flask.Request):
        """
        Returns command from Google Function request.

        :param req: the Google Function request
        :return: returns command from request
        """
        cmd = req.view_args.get('cmd', '')
        try:
            if cmd == '' and req.is_json:
                cmd = req.json.get('cmd', '')
                if cmd == '':
                    cmd = req.args.get('cmd', '')
        except Exception as e:
            # Ignore the error
            pass

        return cmd

    @staticmethod
    def get_parameters(req: flask.Request) -> Parameters:
        """
        Returns body from Google Function request http request.

        :param req: the Google Function request (flask object request)
        :return: returns body from request
        """
        body = req
        try:
            if req.is_json:
                body = req.get_json()
        except Exception as e:
            # Ignore the error
            pass

        return Parameters.from_value(body)
