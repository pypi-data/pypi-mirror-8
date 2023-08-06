import socket
from contextlib import contextmanager

import requests

from . import dispatch
from ._compat import httplib, iteritems

try:
    from contextlib import ExitStack
except ImportError:
    from contextlib2 import ExitStack


class CustomHTTPResponse(Exception):
    def __init__(self, request, code):
        super(CustomHTTPResponse, self).__init__()
        self.response = requests.Response()
        self.response.url = str(request.url)
        self.response.status_code = code
        self.response.reason = httplib.responses.get(code, None)
        self.response.request = request


class FlaskLoopback(object):

    def __init__(self, flask_app):
        super(FlaskLoopback, self).__init__()
        self.flask_app = flask_app
        self._test_client = flask_app.test_client()
        self._request_context_handlers = []
        self._registered_addresses = set()
        self._use_ssl = {}

    def register_request_context_handler(self, handler):
        self._request_context_handlers.append(handler)

    @contextmanager
    def on(self, address, ssl=False):
        self.activate_address(address, ssl)
        try:
            yield self
        finally:
            self.deactivate_address(address)

    def activate_address(self, address, ssl=False):
        assert isinstance(address, tuple) and len(address) == 2, 'Address must be a tuple of the form (host, port)'
        dispatch.register_loopback_handler(address, self, ssl)
        self._registered_addresses.add(address)

    def deactivate_address(self, address):
        assert isinstance(address, tuple) and len(address) == 2, 'Address must be a tuple of the form (host, port)'
        dispatch.unregister_loopback_handler(address)
        self._registered_addresses.remove(address)

    def deactivate_all(self):
        while self._registered_addresses:
            self.deactivate_address(next(iter(self._registered_addresses)))

    def handle_request(self, url, request):
        assert url.scheme
        path = "/{0}".format(url.split("/", 3)[-1])
        open_kwargs = {
            'method': request.method.upper(), 'headers': iteritems(request.headers), 'data': request.body,
            'environ_base': {'REMOTE_ADDR': _get_hostname()},
            'base_url': '{0.scheme}://{0.netloc}'.format(url),
        }
        with ExitStack() as stack:
            for handler in self._request_context_handlers:
                try:
                    stack.enter_context(handler(request))
                except CustomHTTPResponse as e:
                    return e.response

            resp = self._test_client.open(path, **open_kwargs)
            returned = requests.Response()
            assert returned.url is None
            returned.url = str(url)
            returned.status_code = resp.status_code
            returned.reason = httplib.responses.get(resp.status_code, None)
            returned.request = request
            returned._content = resp.get_data()
            returned.headers.update(resp.headers)
            return returned

_hostname = None

def _get_hostname():
    global _hostname
    if _hostname is None:
        _hostname = socket.getfqdn()
    return _hostname
