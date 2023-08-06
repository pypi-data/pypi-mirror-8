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

"""Test the mime_delete handler."""

__all__ = [
    'TestDispose',
    ]


import unittest

from mailman.app.lifecycle import create_list
from mailman.config import config
from mailman.core import errors
from mailman.handlers import mime_delete
from mailman.interfaces.action import FilterAction
from mailman.interfaces.member import MemberRole
from mailman.interfaces.usermanager import IUserManager
from mailman.testing.helpers import (
    LogFileMark, configuration, get_queue_messages,
    specialized_message_from_string as mfs)
from mailman.testing.layers import ConfigLayer
from zope.component import getUtility



class TestDispose(unittest.TestCase):
    """Test the mime_delete handler."""

    layer = ConfigLayer

    def setUp(self):
        self._mlist = create_list('test@example.com')
        self._msg = mfs("""\
From: anne@example.com
To: test@example.com
Subject: A disposable message
Message-ID: <ant>

""")
        config.push('dispose', """
        [mailman]
        site_owner: noreply@example.com
        """)
        # Let assertMultiLineEqual work without bounds.
        self.maxDiff = None

    def tearDown(self):
        config.pop('dispose')

    def test_dispose_discard(self):
        self._mlist.filter_action = FilterAction.discard
        with self.assertRaises(errors.DiscardMessage) as cm:
            mime_delete.dispose(self._mlist, self._msg, {}, 'discarding')
        self.assertEqual(cm.exception.message, 'discarding')
        # There should be no messages in the 'bad' queue.
        self.assertEqual(len(get_queue_messages('bad')), 0)

    def test_dispose_bounce(self):
        self._mlist.filter_action = FilterAction.reject
        with self.assertRaises(errors.RejectMessage) as cm:
            mime_delete.dispose(self._mlist, self._msg, {}, 'rejecting')
        self.assertEqual(cm.exception.message, 'rejecting')
        # There should be no messages in the 'bad' queue.
        self.assertEqual(len(get_queue_messages('bad')), 0)

    def test_dispose_forward(self):
        # The disposed message gets forwarded to the list moderators.  So
        # first add some moderators.
        user_manager = getUtility(IUserManager)
        anne = user_manager.create_address('anne@example.com')
        bart = user_manager.create_address('bart@example.com')
        self._mlist.subscribe(anne, MemberRole.moderator)
        self._mlist.subscribe(bart, MemberRole.moderator)
        # Now set the filter action and dispose the message.
        self._mlist.filter_action = FilterAction.forward
        with self.assertRaises(errors.DiscardMessage) as cm:
            mime_delete.dispose(self._mlist, self._msg, {}, 'forwarding')
        self.assertEqual(cm.exception.message, 'forwarding')
        # There should now be a multipart message in the virgin queue destined
        # for the mailing list owners.
        messages = get_queue_messages('virgin')
        self.assertEqual(len(messages), 1)
        message = messages[0].msg
        self.assertEqual(message.get_content_type(), 'multipart/mixed')
        # Anne and Bart should be recipients of the message, but it will look
        # like the message is going to the list owners.
        self.assertEqual(message['to'], 'test-owner@example.com')
        self.assertEqual(message.recipients,
                         set(['anne@example.com', 'bart@example.com']))
        # The list owner should be the sender.
        self.assertEqual(message['from'], 'noreply@example.com')
        self.assertEqual(message['subject'],
                         'Content filter message notification')
        # The body of the first part provides the moderators some details.
        part0 = message.get_payload(0)
        self.assertEqual(part0.get_content_type(), 'text/plain')
        self.assertMultiLineEqual(part0.get_payload(), """\
The attached message matched the Test mailing list's content
filtering rules and was prevented from being forwarded on to the list
membership.  You are receiving the only remaining copy of the discarded
message.

""")
        # The second part is the container for the original message.
        part1 = message.get_payload(1)
        self.assertEqual(part1.get_content_type(), 'message/rfc822')
        # And the first part of *that* message will be the original message.
        original = part1.get_payload(0)
        self.assertEqual(original['subject'], 'A disposable message')
        self.assertEqual(original['message-id'], '<ant>')

    @configuration('mailman', filtered_messages_are_preservable='no')
    def test_dispose_non_preservable(self):
        # Two actions can happen here, depending on a site-wide setting.  If
        # the site owner has indicated that filtered messages cannot be
        # preserved, then this is the same as discarding them.
        self._mlist.filter_action = FilterAction.preserve
        with self.assertRaises(errors.DiscardMessage) as cm:
            mime_delete.dispose(self._mlist, self._msg, {}, 'not preserved')
        self.assertEqual(cm.exception.message, 'not preserved')
        # There should be no messages in the 'bad' queue.
        self.assertEqual(len(get_queue_messages('bad')), 0)

    @configuration('mailman', filtered_messages_are_preservable='yes')
    def test_dispose_preservable(self):
        # Two actions can happen here, depending on a site-wide setting.  If
        # the site owner has indicated that filtered messages can be
        # preserved, then this is similar to discarding the message except
        # that a copy is preserved in the 'bad' queue.
        self._mlist.filter_action = FilterAction.preserve
        with self.assertRaises(errors.DiscardMessage) as cm:
            mime_delete.dispose(self._mlist, self._msg, {}, 'preserved')
        self.assertEqual(cm.exception.message, 'preserved')
        # There should be no messages in the 'bad' queue.
        messages = get_queue_messages('bad')
        self.assertEqual(len(messages), 1)
        message = messages[0].msg
        self.assertEqual(message['subject'], 'A disposable message')
        self.assertEqual(message['message-id'], '<ant>')

    def test_bad_action(self):
        # This should never happen, but what if it does?
        # FilterAction.accept, FilterAction.hold, and FilterAction.defer are
        # not valid.  They are treated as discard actions, but the problem is
        # also logged.
        for action in (FilterAction.accept,
                       FilterAction.hold,
                       FilterAction.defer):
            self._mlist.filter_action = action
            mark = LogFileMark('mailman.error')
            with self.assertRaises(errors.DiscardMessage) as cm:
                mime_delete.dispose(self._mlist, self._msg, {}, 'bad action')
            self.assertEqual(cm.exception.message, 'bad action')
            line = mark.readline()[:-1]
            self.assertTrue(line.endswith(
                '{0} invalid FilterAction: test@example.com.  '
                'Treating as discard'.format(action.name)))
