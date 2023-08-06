# Copyright (C) 2012-2014 by the Free Software Foundation, Inc.
#
# This file is part of GNU Mailman.
#
# GNU Mailman is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# GNU Mailman is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# GNU Mailman.  If not, see <http://www.gnu.org/licenses/>.

"""Test some Runner base class behavior."""

from __future__ import absolute_import, print_function, unicode_literals

__metaclass__ = type
__all__ = [
    'TestRunner',
    ]


import unittest

from mailman.app.lifecycle import create_list
from mailman.config import config
from mailman.core.runner import Runner
from mailman.interfaces.runner import RunnerCrashEvent
from mailman.runners.virgin import VirginRunner
from mailman.testing.helpers import (
    LogFileMark, configuration, event_subscribers, get_queue_messages,
    make_digest_messages, make_testable_runner,
    specialized_message_from_string as mfs)
from mailman.testing.layers import ConfigLayer



class CrashingRunner(Runner):
    def _dispose(self, mlist, msg, msgdata):
        raise RuntimeError('borked')



class TestRunner(unittest.TestCase):
    """Test the Runner base class behavior."""

    layer = ConfigLayer

    def setUp(self):
        self._mlist = create_list('test@example.com')
        self._events = []

    def _got_event(self, event):
        self._events.append(event)

    @configuration('runner.crashing',
                   **{'class': 'mailman.core.tests.CrashingRunner'})
    def test_crash_event(self):
        runner = make_testable_runner(CrashingRunner, 'in')
        # When an exception occurs in Runner._process_one_file(), a zope.event
        # gets triggered containing the exception object.
        msg = mfs("""\
From: anne@example.com
To: test@example.com
Message-ID: <ant>

""")
        config.switchboards['in'].enqueue(msg, listname='test@example.com')
        with event_subscribers(self._got_event):
            runner.run()
        # We should now have exactly one event, which will contain the
        # exception, plus additional metadata containing the mailing list,
        # message, and metadata.
        self.assertEqual(len(self._events), 1)
        event = self._events[0]
        self.assertTrue(isinstance(event, RunnerCrashEvent))
        self.assertEqual(event.mailing_list, self._mlist)
        self.assertEqual(event.message['message-id'], '<ant>')
        self.assertEqual(event.metadata['listname'], 'test@example.com')
        self.assertTrue(isinstance(event.error, RuntimeError))
        self.assertEqual(str(event.error), 'borked')
        self.assertTrue(isinstance(event.runner, CrashingRunner))
        # The message should also have ended up in the shunt queue.
        shunted = get_queue_messages('shunt')
        self.assertEqual(len(shunted), 1)
        self.assertEqual(shunted[0].msg['message-id'], '<ant>')

    def test_digest_messages(self):
        # In LP: #1130697, the digest runner creates MIME digests using the
        # stdlib MIMEMutlipart class, however this class does not have the
        # extended attributes we require (e.g. .sender).  The fix is to use a
        # subclass of MIMEMultipart and our own Message subclass; this adds
        # back the required attributes.  (LP: #1130696)
        #
        # Start by creating the raw ingredients for the digests.  This also
        # runs the digest runner, thus producing the digest messages into the
        # virgin queue.
        make_digest_messages(self._mlist)
        # Run the virgin queue processor, which runs the cook-headers and
        # to-outgoing handlers.  This should produce no error.
        error_log = LogFileMark('mailman.error')
        runner = make_testable_runner(VirginRunner, 'virgin')
        runner.run()
        error_text = error_log.read()
        self.assertEqual(len(error_text), 0, error_text)
        self.assertEqual(len(get_queue_messages('shunt')), 0)
        messages = get_queue_messages('out')
        self.assertEqual(len(messages), 2)
        # Which one is the MIME digest?
        mime_digest = None
        for bag in messages:
            if bag.msg.get_content_type() == 'multipart/mixed':
                assert mime_digest is None, 'Found two MIME digests'
                mime_digest = bag.msg
        # The cook-headers handler ran.
        self.assertIn('x-mailman-version', mime_digest)
        self.assertEqual(mime_digest['precedence'], 'list')
        # The list's -request address is the original sender.
        self.assertEqual(bag.msgdata['original_sender'],
                         'test-request@example.com')
