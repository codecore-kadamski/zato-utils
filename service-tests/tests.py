from example_service import MyServiceUsingInvoke
from example_service import MyServiceUsingOutgoingSoapConnection
from example_service import MyServiceUsingOutgoingHTTPConnection
import httplib
import uuid
import unittest
from mock import Mock
from datetime import datetime

"""

"""


def mock_response(status_code, content, raise_error=False):
    """
        Creates a mock response from the outgoing http server

        This will return a basic requests object with the status code
        and the response text as well as the .json() return value
    """

    response = Mock()
    response.status_code = status_code
    response.json.return_value = content
    response.text = content
    if raise_error:
        # If you want to test what will happen if malformatted json is passed
        response.json.side_effect = Exception("Error Converting Json")
    return response


def mock_setup_service(service, payload, headers={}, mocked_response=Mock()):

    """
        This is used for http outgoing tests.

        Sets up a mock service with params.
        This function will then call before_handle()

        You can pass through a request.payload and it will assign it to
        the service.

        The headers are for the outgoing http request if needed.
        mocked response is the response of the outgoing http request

        This function will assign all the values to the zato service for you
        so that you can test your code effeciently

    """
    service.request.payload = payload
    service.wsgi_environ = headers
    service.cid = str(uuid.uuid4())
    service.before_handle()

    conn = Mock()
    conn.conn.get.status_code = mocked_response.status_code
    conn.conn.get.return_value = mocked_response

    conn.conn.post.status_code = mocked_response.status_code
    conn.conn.post.return_value = mocked_response

    conn.conn.patch.status_code = mocked_response.status_code
    conn.conn.patch.return_value = mocked_response

    return service


class MyServiceUsingInvokeTestCase(unittest.TestCase):

    # This test will never pass because we don't catch the error in the service
    def test_error_on_invoke(self):
        service = MyServiceUsingInvoke()
        service.invoke.side_effect = Exception("This is a forced error")
        service.handle()
        self.assertEqual(service.response.payload, None)


class MyServiceUsingOutgoingSoapConnectionTestCase(unittest.TestCase):

    def setUp(self):
        """
            With outgoing soap services there is a bit of setup needed
            1We need to mock the entire soap request and its response.
        """
        self.service = MyServiceUsingOutgoingSoapConnection()
        self.now_time = datetime.now()
        self.mock_client = Mock()
        self.mock_client.service.GetTheTimeRightNow.return_value = self.now_time  # noqa

        self.service.outgoing.soap[
            'get-date-time'
        ].conn.client().return_value = self.mock_client

        # Because we are using the with clause, we need to mock enter and exit
        self.service.outgoing.soap[
            'get-date-time'
        ].conn.client().__exit__ = Mock()

        self.service.outgoing.soap[
            'get-date-time'
        ].conn.client().__enter__ = Mock()

    def test_handle(self):
        self.service.before_handle()
        self.service.handle()
        self.service.after_handle()
        assert self.service.response.payload == {'time': self.now_time}


class MyServiceUsingOutgoingHTTPConnectionTestCase(unittest.TestCase):

    def test_handle(self):
        # Set up the service, mock the http response to return datetime
        outgoing_http_response_value = {'date': datetime.now()}
        service = mock_setup_service(
            MyServiceUsingOutgoingHTTPConnection(),
            {},
            # Set the outgoing http mock to return the datetime.
            # Make sure that your mocked response is in the same format as to
            # what an api request to the outgoing http server would be.
            # ie. keep your schema consistant.
            mock_response(httplib.OK, outgoing_http_response_value)
        )

        # Run the handle
        service.handle()

        # Run tests on the response
        assert 'date' in service.response.payload
        assert service.response.payload == outgoing_http_response_value
