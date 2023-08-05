
from assertions import *

from mox import MoxTestBase, IsA
from gevent.socket import socket
from gevent.ssl import SSLError

from slimta.smtp.server import Server
from slimta.smtp.auth import AuthSession, CredentialsInvalidError
from slimta.smtp.auth.standard import Plain
from slimta.smtp import ConnectionLost


class FakeAuth(object):

    def verify_secret(self, cid, secret, zid=None):
        if cid != 'testuser' or secret != 'testpassword':
            raise CredentialsInvalidError()
        if zid is not None and zid != 'testzid':
            raise CredentialsInvalidError()
        return (cid, zid)

    def get_available_mechanisms(self, encrypted=False):
        return [Plain]


class TestSmtpServer(MoxTestBase):

    def setUp(self):
        super(TestSmtpServer, self).setUp()
        self.sock = self.mox.CreateMock(socket)
        self.sock.fileno = lambda: -1
        self.tls_args = {'server_side': True}

    def test_starttls_extension(self):
        s = Server(None, None)
        assert_false('STARTTLS' in s.extensions)
        s = Server(None, None, tls=self.tls_args, tls_immediately=False)
        assert_true('STARTTLS' in s.extensions)
        s = Server(None, None, tls=self.tls_args, tls_immediately=True)
        assert_false('STARTTLS' in s.extensions)

    def test_recv_command(self):
        self.sock.recv(IsA(int)).AndReturn('cmd ARG\r\n')
        self.mox.ReplayAll()
        s = Server(self.sock, None)
        cmd, arg = s._recv_command()
        assert_equal('CMD', cmd)
        assert_equal('ARG', arg)

    def test_get_message_data(self):
        expected_reply = '250 2.6.0 Message Accepted for Delivery\r\n'
        self.sock.recv(IsA(int)).AndReturn('one\r\n')
        self.sock.recv(IsA(int)).AndReturn('.\r\n')
        self.sock.sendall(expected_reply)
        self.mox.ReplayAll()
        s = Server(self.sock, None)
        s._get_message_data()
        assert_false(s.have_mailfrom)
        assert_false(s.have_rcptto)

    def test_call_custom_handler(self):
        class TestHandler(object):
            def TEST(self, arg):
                return arg.lower()
        s = Server(None, TestHandler())
        assert_equal('stuff', s._call_custom_handler('TEST', 'STUFF'))

    def test_banner_quit(self):
        self.sock.sendall('220 ESMTP server\r\n')
        self.sock.recv(IsA(int)).AndReturn('QUIT\r\n')
        self.sock.sendall('221 2.0.0 Bye\r\n')
        self.mox.ReplayAll()
        s = Server(self.sock, None)
        s.handle()

    def test_unhandled_error(self):
        class TestHandler(object):
            def BANNER_(self, reply):
                raise Exception('test')
        self.sock.sendall('421 4.3.0 Unhandled system error\r\n')
        self.mox.ReplayAll()
        s = Server(self.sock, TestHandler())
        with assert_raises(Exception) as cm:
            s.handle()
        assert_equal(('test', ), cm.exception.args)

    def test_banner_command(self):
        self.sock.sendall('220 ESMTP server\r\n')
        self.sock.recv(IsA(int)).AndReturn('BANNER\r\n')
        self.sock.sendall('500 5.5.2 Syntax error, command unrecognized\r\n')
        self.sock.recv(IsA(int)).AndReturn('BANNER_\r\n')
        self.sock.sendall('500 5.5.2 Syntax error, command unrecognized\r\n')
        self.sock.recv(IsA(int)).AndReturn('QUIT\r\n')
        self.sock.sendall('221 2.0.0 Bye\r\n')
        self.mox.ReplayAll()
        s = Server(self.sock, None)
        s.handle()

    def test_tls_immediately(self):
        sock = self.mox.CreateMockAnything()
        sock.fileno = lambda: -1
        sock.tls_wrapper(sock, self.tls_args).AndReturn(sock)
        sock.sendall('220 ESMTP server\r\n')
        sock.recv(IsA(int)).AndReturn('QUIT\r\n')
        sock.sendall('221 2.0.0 Bye\r\n')
        self.mox.ReplayAll()
        s = Server(sock, None, tls=self.tls_args, tls_immediately=True,
                               tls_wrapper=sock.tls_wrapper)
        s.handle()

    def test_tls_immediately_sslerror(self):
        sock = self.mox.CreateMockAnything()
        sock.fileno = lambda: -1
        sock.tls_wrapper(sock, self.tls_args).AndRaise(SSLError())
        sock.sendall('421 4.7.0 TLS negotiation failed\r\n')
        self.mox.ReplayAll()
        s = Server(sock, None, tls=self.tls_args, tls_immediately=True,
                               tls_wrapper=sock.tls_wrapper)
        s.handle()

    def test_ehlo(self):
        self.sock.sendall('220 ESMTP server\r\n')
        self.sock.recv(IsA(int)).AndReturn('EHLO there\r\n')
        self.sock.sendall('250-Hello there\r\n250 TEST\r\n')
        self.sock.recv(IsA(int)).AndReturn('QUIT\r\n')
        self.sock.sendall('221 2.0.0 Bye\r\n')
        self.mox.ReplayAll()
        s = Server(self.sock, None)
        s.extensions.reset()
        s.extensions.add('TEST')
        s.handle()
        assert_equal('there', s.ehlo_as)

    def test_helo(self):
        self.sock.sendall('220 ESMTP server\r\n')
        self.sock.recv(IsA(int)).AndReturn('HELO there\r\n')
        self.sock.sendall('250 Hello there\r\n')
        self.sock.recv(IsA(int)).AndReturn('QUIT\r\n')
        self.sock.sendall('221 2.0.0 Bye\r\n')
        self.mox.ReplayAll()
        s = Server(self.sock, None)
        s.handle()
        assert_equal('there', s.ehlo_as)

    def test_starttls(self):
        sock = self.mox.CreateMockAnything()
        sock.fileno = lambda: -1
        sock.sendall('220 ESMTP server\r\n')
        sock.recv(IsA(int)).AndReturn('EHLO there\r\n')
        sock.sendall('250-Hello there\r\n250 STARTTLS\r\n')
        sock.recv(IsA(int)).AndReturn('STARTTLS\r\n')
        sock.sendall('220 2.7.0 Go ahead\r\n')
        sock.tls_wrapper(sock, self.tls_args).AndReturn(sock)
        sock.recv(IsA(int)).AndReturn('QUIT\r\n')
        sock.sendall('221 2.0.0 Bye\r\n')
        self.mox.ReplayAll()
        s = Server(sock, None, tls=self.tls_args, tls_wrapper=sock.tls_wrapper)
        s.extensions.reset()
        s.extensions.add('STARTTLS')
        s.handle()
        assert_equal(None, s.ehlo_as)

    def test_starttls_bad(self):
        sock = self.mox.CreateMockAnything()
        sock.fileno = lambda: -1
        sock.sendall('220 ESMTP server\r\n')
        sock.recv(IsA(int)).AndReturn('STARTTLS\r\n')
        sock.sendall('503 5.5.1 Bad sequence of commands\r\n')
        sock.recv(IsA(int)).AndReturn('STARTTLS badarg\r\n')
        sock.sendall('501 5.5.4 Syntax error in parameters or arguments\r\n')
        sock.recv(IsA(int)).AndReturn('EHLO there\r\n')
        sock.sendall('250-Hello there\r\n250 STARTTLS\r\n')
        sock.recv(IsA(int)).AndReturn('STARTTLS\r\n')
        sock.sendall('220 2.7.0 Go ahead\r\n')
        sock.tls_wrapper(sock, self.tls_args).AndRaise(SSLError())
        sock.sendall('421 4.7.0 TLS negotiation failed\r\n')
        self.mox.ReplayAll()
        s = Server(sock, None, tls=self.tls_args, tls_wrapper=sock.tls_wrapper)
        s.extensions.reset()
        s.extensions.add('STARTTLS')
        s.handle()
        assert_equal('there', s.ehlo_as)

    def test_auth(self):
        self.sock.sendall('220 ESMTP server\r\n')
        self.sock.recv(IsA(int)).AndReturn('EHLO there\r\n')
        self.sock.sendall('250-Hello there\r\n250 AUTH PLAIN\r\n')
        self.sock.recv(IsA(int)).AndReturn('AUTH PLAIN dGVzdHppZAB0ZXN0dXNlcgB0ZXN0cGFzc3dvcmQ=\r\n')
        self.sock.sendall('235 2.7.0 Authentication successful\r\n')
        self.sock.recv(IsA(int)).AndReturn('QUIT\r\n')
        self.sock.sendall('221 2.0.0 Bye\r\n')
        self.mox.ReplayAll()
        s = Server(self.sock, None)
        s.extensions.reset()
        s.extensions.add('AUTH', AuthSession(FakeAuth(), s))
        s.handle()
        assert_equal(('testuser', 'testzid'), s.auth_result)

    def test_mailfrom(self):
        self.sock.sendall('220 ESMTP server\r\n')
        self.sock.recv(IsA(int)).AndReturn('HELO there\r\n')
        self.sock.sendall('250 Hello there\r\n')
        self.sock.recv(IsA(int)).AndReturn('MAIL FROM:<test">"addr>\r\n')
        self.sock.sendall('250 2.1.0 Sender <test">"addr> Ok\r\n')
        self.sock.recv(IsA(int)).AndReturn('QUIT\r\n')
        self.sock.sendall('221 2.0.0 Bye\r\n')
        self.mox.ReplayAll()
        s = Server(self.sock, None)
        s.handle()
        assert_true(s.have_mailfrom)

    def test_mailfrom_bad(self):
        self.sock.sendall('220 ESMTP server\r\n')
        self.sock.recv(IsA(int)).AndReturn('MAIL FROM:<test>\r\n')
        self.sock.sendall('503 5.5.1 Bad sequence of commands\r\n')
        self.sock.recv(IsA(int)).AndReturn('HELO there\r\n')
        self.sock.sendall('250 Hello there\r\n')
        self.sock.recv(IsA(int)).AndReturn('MAIL FROM:<test1> SIZE=5\r\n')
        self.sock.sendall('504 5.5.4 Command parameter not implemented\r\n')
        self.sock.recv(IsA(int)).AndReturn('MAIL FRM:<addr>\r\n')
        self.sock.sendall('501 5.5.4 Syntax error in parameters or arguments\r\n')
        self.sock.recv(IsA(int)).AndReturn('MAIL FROM:<addr\r\n')
        self.sock.sendall('501 5.5.4 Syntax error in parameters or arguments\r\n')
        self.sock.recv(IsA(int)).AndReturn('MAIL FROM:<test1>\r\n')
        self.sock.sendall('250 2.1.0 Sender <test1> Ok\r\n')
        self.sock.recv(IsA(int)).AndReturn('MAIL FROM:<test2>\r\n')
        self.sock.sendall('503 5.5.1 Bad sequence of commands\r\n')
        self.sock.recv(IsA(int)).AndReturn('QUIT\r\n')
        self.sock.sendall('221 2.0.0 Bye\r\n')
        self.mox.ReplayAll()
        s = Server(self.sock, None)
        s.handle()
        assert_true(s.have_mailfrom)

    def test_mailfrom_send_extension(self):
        self.sock.sendall('220 ESMTP server\r\n')
        self.sock.recv(IsA(int)).AndReturn('EHLO there\r\n')
        self.sock.sendall('250-Hello there\r\n250 SIZE 10\r\n')
        self.sock.recv(IsA(int)).AndReturn('MAIL FROM:<test1> SIZE=ASDF\r\n')
        self.sock.sendall('501 5.5.4 Syntax error in parameters or arguments\r\n')
        self.sock.recv(IsA(int)).AndReturn('MAIL FROM:<test1> SIZE=20\r\n')
        self.sock.sendall('552 5.3.4 Message size exceeds 10 limit\r\n')
        self.sock.recv(IsA(int)).AndReturn('MAIL FROM:<test1> SIZE=5\r\n')
        self.sock.sendall('250 2.1.0 Sender <test1> Ok\r\n')
        self.sock.recv(IsA(int)).AndReturn('QUIT\r\n')
        self.sock.sendall('221 2.0.0 Bye\r\n')
        self.mox.ReplayAll()
        s = Server(self.sock, None)
        s.extensions.reset()
        s.extensions.add('SIZE', 10)
        s.handle()
        assert_true(s.have_mailfrom)

    def test_rcptto(self):
        self.sock.sendall('220 ESMTP server\r\n')
        self.sock.recv(IsA(int)).AndReturn('RCPT TO:<test">"addr>\r\n')
        self.sock.sendall('250 2.1.5 Recipient <test">"addr> Ok\r\n')
        self.sock.recv(IsA(int)).AndReturn('RCPT TO:<test2>\r\n')
        self.sock.sendall('250 2.1.5 Recipient <test2> Ok\r\n')
        self.sock.recv(IsA(int)).AndReturn('QUIT\r\n')
        self.sock.sendall('221 2.0.0 Bye\r\n')
        self.mox.ReplayAll()
        s = Server(self.sock, None)
        s.ehlo_as = 'test'
        s.have_mailfrom = True
        s.handle()
        assert_true(s.have_rcptto)

    def test_rcptto_bad(self):
        self.sock.sendall('220 ESMTP server\r\n')
        self.sock.recv(IsA(int)).AndReturn('RCPT TO:<test>\r\n')
        self.sock.sendall('503 5.5.1 Bad sequence of commands\r\n')
        self.sock.recv(IsA(int)).AndReturn('HELO there\r\n')
        self.sock.sendall('250 Hello there\r\n')
        self.sock.recv(IsA(int)).AndReturn('RCPT TO:<test>\r\n')
        self.sock.sendall('503 5.5.1 Bad sequence of commands\r\n')
        self.sock.recv(IsA(int)).AndReturn('MAIL FROM:<test1>\r\n')
        self.sock.sendall('250 2.1.0 Sender <test1> Ok\r\n')
        self.sock.recv(IsA(int)).AndReturn('RCPT T:<test1>\r\n')
        self.sock.sendall('501 5.5.4 Syntax error in parameters or arguments\r\n')
        self.sock.recv(IsA(int)).AndReturn('RCPT TO:<test1\r\n')
        self.sock.sendall('501 5.5.4 Syntax error in parameters or arguments\r\n')
        self.sock.recv(IsA(int)).AndReturn('QUIT\r\n')
        self.sock.sendall('221 2.0.0 Bye\r\n')
        self.mox.ReplayAll()
        s = Server(self.sock, None)
        s.handle()
        assert_false(s.have_rcptto)

    def test_data(self):
        self.sock.sendall('220 ESMTP server\r\n')
        self.sock.recv(IsA(int)).AndReturn('DATA\r\n')
        self.sock.sendall('354 Start mail input; end with <CRLF>.<CRLF>\r\n')
        self.sock.recv(IsA(int)).AndReturn('.\r\nQUIT\r\n')
        self.sock.sendall('250 2.6.0 Message Accepted for Delivery\r\n')
        self.sock.sendall('221 2.0.0 Bye\r\n')
        self.mox.ReplayAll()
        s = Server(self.sock, None)
        s.ehlo_as = 'test'
        s.have_mailfrom = True
        s.have_rcptto = True
        s.handle()

    def test_data_bad(self):
        self.sock.sendall('220 ESMTP server\r\n')
        self.sock.recv(IsA(int)).AndReturn('DATA arg\r\n')
        self.sock.sendall('501 5.5.4 Syntax error in parameters or arguments\r\n')
        self.sock.recv(IsA(int)).AndReturn('DATA\r\n')
        self.sock.sendall('503 5.5.1 Bad sequence of commands\r\n')
        self.sock.recv(IsA(int)).AndReturn('QUIT\r\n')
        self.sock.sendall('221 2.0.0 Bye\r\n')
        self.mox.ReplayAll()
        s = Server(self.sock, None)
        s.ehlo_as = 'test'
        s.have_mailfrom = True
        s.handle()

    def test_data_connectionlost(self):
        self.sock.sendall('220 ESMTP server\r\n')
        self.sock.recv(IsA(int)).AndReturn('DATA\r\n')
        self.sock.sendall('354 Start mail input; end with <CRLF>.<CRLF>\r\n')
        self.sock.recv(IsA(int)).AndReturn('')
        self.mox.ReplayAll()
        s = Server(self.sock, None)
        s.ehlo_as = 'test'
        s.have_mailfrom = True
        s.have_rcptto = True
        assert_raises(ConnectionLost, s.handle)

    def test_noop(self):
        self.sock.sendall('220 ESMTP server\r\n')
        self.sock.recv(IsA(int)).AndReturn('NOOP\r\n')
        self.sock.sendall('250 2.0.0 Ok\r\n')
        self.sock.recv(IsA(int)).AndReturn('QUIT\r\n')
        self.sock.sendall('221 2.0.0 Bye\r\n')
        self.mox.ReplayAll()
        s = Server(self.sock, None)
        s.handle()

    def test_rset(self):
        class TestHandlers(object):
            server = None
            def NOOP(self2, reply):
                assert_equal('test', self2.server.ehlo_as)
                assert_false(self2.server.have_mailfrom)
                assert_false(self2.server.have_rcptto)
        self.sock.sendall('220 ESMTP server\r\n')
        self.sock.recv(IsA(int)).AndReturn('RSET arg\r\n')
        self.sock.sendall('501 5.5.4 Syntax error in parameters or arguments\r\n')
        self.sock.recv(IsA(int)).AndReturn('RSET\r\n')
        self.sock.sendall('250 2.0.0 Ok\r\n')
        self.sock.recv(IsA(int)).AndReturn('NOOP\r\n')
        self.sock.sendall('250 2.0.0 Ok\r\n')
        self.sock.recv(IsA(int)).AndReturn('QUIT\r\n')
        self.sock.sendall('221 2.0.0 Bye\r\n')
        self.mox.ReplayAll()
        h = TestHandlers()
        s = h.server = Server(self.sock, h)
        s.ehlo_as = 'test'
        s.have_mailfrom = True
        s.have_rcptto = True
        s.handle()

    def test_quit_bad(self):
        self.sock.sendall('220 ESMTP server\r\n')
        self.sock.recv(IsA(int)).AndReturn('QUIT arg\r\n')
        self.sock.sendall('501 5.5.4 Syntax error in parameters or arguments\r\n')
        self.sock.recv(IsA(int)).AndReturn('QUIT\r\n')
        self.sock.sendall('221 2.0.0 Bye\r\n')
        self.mox.ReplayAll()
        s = Server(self.sock, None)
        s.handle()

    def test_custom_command(self):
        class TestHandlers(object):
            def TEST(self2, reply, arg, server):
                assert_true(server.have_mailfrom)
                reply.code = '250'
                reply.message = 'Doing '+arg
        self.sock.sendall('220 ESMTP server\r\n')
        self.sock.recv(IsA(int)).AndReturn('TEST stuff\r\n')
        self.sock.sendall('250 2.0.0 Doing stuff\r\n')
        self.sock.recv(IsA(int)).AndReturn('QUIT\r\n')
        self.sock.sendall('221 2.0.0 Bye\r\n')
        self.mox.ReplayAll()
        s = Server(self.sock, TestHandlers())
        s.have_mailfrom = True
        s.handle()

    def test_bad_commands(self):
        self.sock.sendall('220 ESMTP server\r\n')
        self.sock.recv(IsA(int)).AndReturn('\r\n')
        self.sock.sendall('500 5.5.2 Syntax error, command unrecognized\r\n')
        self.sock.recv(IsA(int)).AndReturn('BADCMD\r\n')
        self.sock.sendall('500 5.5.2 Syntax error, command unrecognized\r\n')
        self.sock.recv(IsA(int)).AndReturn('STARTTLS\r\n')
        self.sock.sendall('500 5.5.2 Syntax error, command unrecognized\r\n')
        self.sock.recv(IsA(int)).AndReturn('AUTH\r\n')
        self.sock.sendall('500 5.5.2 Syntax error, command unrecognized\r\n')
        self.sock.recv(IsA(int)).AndReturn('QUIT\r\n')
        self.sock.sendall('221 2.0.0 Bye\r\n')
        self.mox.ReplayAll()
        s = Server(self.sock, None)
        s.handle()

    def test_gather_params(self):
        s = Server(None, None)
        assert_equal({'ONE': '1'}, s._gather_params(' ONE=1'))
        assert_equal({'TWO': True}, s._gather_params('TWO'))
        assert_equal({'THREE': 'foo', 'FOUR': 'bar'}, s._gather_params(' THREE=foo FOUR=bar'))
        assert_equal({'FIVE': True}, s._gather_params('five'))


# vim:et:fdm=marker:sts=4:sw=4:ts=4
