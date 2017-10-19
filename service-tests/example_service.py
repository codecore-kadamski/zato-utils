# -*- coding: utf-8 -*-
from __future__ import absolute_import, division
from __future__ import print_function, unicode_literals
import json

try:
    from zato.server.service import Service
except ImportError:
    # Override for unit tests
    from mock import Mock

    class Service:
        wsgi_environ = {}
        request = Mock()
        environ = {}
        request.payload = {}
        request.http.GET = {}
        response = Mock()
        response.payload = {}
        log_input = Mock()
        log_output = Mock()
        logger = Mock()
        cid = Mock()
        outgoing = Mock()
        outgoing.plain_http = {}
        outgoing.soap = {}
        cid = Mock()
        invoke = Mock()


class MyServiceUsingInvoke(Service):

    def before_handle(self):
        self.log_input()

    def handle(self):
        response = json.loads(self.invoke('get-date-time'))
        self.response.payload = response

    def after_handle(self):
        self.log_output()


class MyServiceUsingOutgoingSoapConnection(Service):

    def before_handle(self):
        self.log_input()

    def handle(self):
        with self.outgoing.soap[self.environ['wsdl']].conn.client() as client:

            _time = client.service.GetTheTimeRightNow()
            self.response.payload = {'time': _time}

    def after_handle(self):
        self.log_output()


class MyServiceUsingOutgoingHTTPConnection(Service):

    def before_handle(self):
        self.log_input()

    def handle(self):
        service = self.outgoing.plain_http['get-date-time'].conn
        response = service.get(self.cid)
        self.response.payload = response

    def after_handle(self):
        self.log_output()

