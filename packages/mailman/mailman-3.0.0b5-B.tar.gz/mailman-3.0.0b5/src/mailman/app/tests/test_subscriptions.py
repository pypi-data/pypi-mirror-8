# Copyright (C) 2011-2014 by the Free Software Foundation, Inc.
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

"""Tests for the subscription service."""

__all__ = [
    'TestJoin'
    ]


import uuid
import unittest

from mailman.app.lifecycle import create_list
from mailman.interfaces.address import InvalidEmailAddressError
from mailman.interfaces.member import MemberRole, MissingPreferredAddressError
from mailman.interfaces.subscriptions import (
    MissingUserError, ISubscriptionService)
from mailman.testing.layers import ConfigLayer
from zope.component import getUtility



class TestJoin(unittest.TestCase):
    layer = ConfigLayer

    def setUp(self):
        self._mlist = create_list('test@example.com')
        self._service = getUtility(ISubscriptionService)

    def test_join_user_with_bogus_id(self):
        # When `subscriber` is a missing user id, an exception is raised.
        with self.assertRaises(MissingUserError) as cm:
            self._service.join('test.example.com', uuid.UUID(int=99))
        self.assertEqual(cm.exception.user_id, uuid.UUID(int=99))

    def test_join_user_with_invalid_email_address(self):
        # When `subscriber` is a string that is not an email address, an
        # exception is raised.
        with self.assertRaises(InvalidEmailAddressError) as cm:
            self._service.join('test.example.com', 'bogus')
        self.assertEqual(cm.exception.email, 'bogus')

    def test_missing_preferred_address(self):
        # A user cannot join a mailing list if they have no preferred address.
        anne = self._service.join(
            'test.example.com', 'anne@example.com', 'Anne Person')
        # Try to join Anne as a user with a different role.  Her user has no
        # preferred address, so this will fail.
        self.assertRaises(MissingPreferredAddressError,
                          self._service.join,
                          'test.example.com', anne.user.user_id,
                          role=MemberRole.owner)
