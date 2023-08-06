
from assertions import *

from mox import MoxTestBase, IsA
import gevent
from gevent.pywsgi import WSGIServer as GeventWSGIServer

from slimta.http.wsgi import WsgiServer, log


class TestWsgiServer(MoxTestBase):

    def test_build_server(self):
        w = WsgiServer()
        server = w.build_server(('0.0.0.0', 0))
        assert_is_instance(server, GeventWSGIServer)

    def test_handle_unimplemented(self):
        w = WsgiServer()
        with assert_raises(NotImplementedError):
            w.handle(None, None)

    def test_call(self):
        class FakeWsgiServer(WsgiServer):
            def handle(self, environ, start_response):
                start_response('200 Test', 13)
                return ['test']
        w = FakeWsgiServer()
        environ = {}
        start_response = self.mox.CreateMockAnything()
        self.mox.StubOutWithMock(log, 'wsgi_request')
        self.mox.StubOutWithMock(log, 'wsgi_response')
        log.wsgi_request(environ)
        start_response('200 Test', 13)
        log.wsgi_response(environ, '200 Test', 13)
        self.mox.ReplayAll()
        assert_equal(['test'], w(environ, start_response))


# vim:et:fdm=marker:sts=4:sw=4:ts=4
