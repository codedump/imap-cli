# -*- coding: utf-8 -*-


"""Test helpers"""


import copy
import email
import imaplib
import unittest

import six

from imap_cli import fetch
from imap_cli import tests


class FetchTest(unittest.TestCase):
    reference_mail = {
        u'headers': {
            u'From': u'exampleFrom <example@from.org>',
            u'Content-Transfer-Encoding': u'quoted-printable',
            u'To': u'exampleTo <example@to.org>',
            u'Date': u'Tue, 03 Jan 1989 09:42:34 +0200',
            u'Subject': u'Mocking IMAP Protocols',
            u'Content-Type': u'text/html;\r\n\tcharset="windows-1252"',
            u'MIME-Version': u'1.0'
        },
        u'parts': [
            {
                u'as_string': u'\n'.join([
                    u'From: exampleFrom <example@from.org>',
                    u'Date: Tue, 03 Jan 1989 09:42:34 +0200',
                    u'Subject: Mocking IMAP Protocols',
                    u'To: exampleTo <example@to.org>',
                    u'MIME-Version: 1.0',
                    u'Content-Type: text/html;',
                    u'\tcharset="windows-1252"',
                    u'Content-Transfer-Encoding: quoted-printable',
                    u'',
                    u'EMAIL BODY CONTENT',
                ]),
                u'data': u'\n'.join([
                    u'From: exampleFrom <example@from.org>',
                    u'Date: Tue, 03 Jan 1989 09:42:34 +0200',
                    u'Subject: Mocking IMAP Protocols',
                    u'To: exampleTo <example@to.org>',
                    u'MIME-Version: 1.0',
                    u'Content-Type: text/html;',
                    u'\tcharset="windows-1252"',
                    u'Content-Transfer-Encoding: quoted-printable',
                    u'',
                    u'EMAIL BODY CONTENT',
                ]),
                u'content_type': 'text/html'
            }
        ]
    }

    def setUp(self):
        imaplib.IMAP4_SSL = tests.ImapConnectionMock()

    def test_display(self):
        assert isinstance(fetch.display(self.reference_mail), six.string_types)

    def test_get_charset(self):
        multipart_mail = copy.deepcopy(self.reference_mail)
        multipart_mail['parts'].append({
            u'content_type': u'img/png',
            u'data': u'xxxxxx',
            u'filename': 'IMGTEST',
        })

        mail = email.message_from_string(self.reference_mail['parts'][0]['data'])
        assert fetch.get_charset(mail) == 'windows-1252'

    def test_read(self):
        self.imap_account = imaplib.IMAP4_SSL()
        self.imap_account.login()

        mail = fetch.read(self.imap_account, 1, directory="INBOX")

        for header_name, header_value in mail['headers'].items():
            assert self.reference_mail['headers'][header_name] == header_value
        assert len(mail['parts']) == len(self.reference_mail['parts'])
