
import unittest
import re

from assertions import *

from slimta.policy.headers import AddDateHeader, AddMessageIdHeader, \
                                  AddReceivedHeader
from slimta.envelope import Envelope


class TestPolicyHeaders(unittest.TestCase):

    def test_add_date_header(self):
        env = Envelope()
        env.parse('')
        env.timestamp = 1234567890
        adh = AddDateHeader()
        assert_equal(None, env.headers['Date'])
        adh.apply(env)
        assert_true(env.headers['Date'])

    def test_add_date_header_existing(self):
        env = Envelope()
        env.parse('Date: testing\r\n')
        adh = AddDateHeader()
        assert_equal('testing', env.headers['Date'])
        adh.apply(env)
        assert_equal('testing', env.headers['Date'])

    def test_add_message_id_header(self):
        env = Envelope()
        env.parse('')
        env.timestamp = 1234567890
        amih = AddMessageIdHeader('example.com')
        assert_equal(None, env.headers['Message-Id'])
        amih.apply(env)
        pattern = r'^<[0-9a-fA-F]{32}\.1234567890@example.com>$'
        assert_regexp_matches(env.headers['Message-Id'], pattern)

    def test_add_message_id_header_existing(self):
        env = Envelope()
        env.parse('Message-Id: testing\r\n')
        amih = AddMessageIdHeader()
        assert_equal('testing', env.headers['Message-Id'])
        amih.apply(env)
        assert_equal('testing', env.headers['Message-Id'])

    def test_add_received_header(self):
        env = Envelope('sender@example.com', ['rcpt@example.com'])
        env.parse('From: test@example.com\r\n')
        env.timestamp = 1234567890
        env.client['name'] = 'mail.example.com'
        env.client['ip'] = '1.2.3.4'
        env.client['protocol'] = 'ESMTPS'
        env.receiver = 'test.com'
        arh = AddReceivedHeader()
        arh.apply(env)
        assert_regexp_matches(env.headers['Received'],
                r'from mail\.example\.com \(unknown \[1.2.3.4\]\) by test.com '
                r'\(slimta [^\)]+\) with ESMTPS for <rcpt@example.com>; ')

    def test_add_received_header_prepended(self):
        env = Envelope('sender@example.com', ['rcpt@example.com'])
        env.parse('From: test@example.com\r\n')
        AddReceivedHeader().apply(env)
        assert_equal(['Received', 'From'], env.headers.keys())


# vim:et:fdm=marker:sts=4:sw=4:ts=4
