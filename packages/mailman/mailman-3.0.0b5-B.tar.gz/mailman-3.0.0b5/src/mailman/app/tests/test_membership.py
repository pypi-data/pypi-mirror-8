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

"""Tests of application level membership functions."""

__all__ = [
    'TestAddMember',
    'TestAddMemberPassword',
    'TestDeleteMember',
    ]


import unittest

from mailman.app.lifecycle import create_list
from mailman.app.membership import add_member, delete_member
from mailman.core.constants import system_preferences
from mailman.interfaces.bans import IBanManager
from mailman.interfaces.member import (
    AlreadySubscribedError, DeliveryMode, MemberRole, MembershipIsBannedError,
    NotAMemberError)
from mailman.interfaces.usermanager import IUserManager
from mailman.testing.layers import ConfigLayer
from zope.component import getUtility



class TestAddMember(unittest.TestCase):
    layer = ConfigLayer

    def setUp(self):
        self._mlist = create_list('test@example.com')

    def test_add_member_new_user(self):
        # Test subscribing a user to a mailing list when the email address has
        # not yet been associated with a user.
        member = add_member(self._mlist, 'aperson@example.com',
                            'Anne Person', '123', DeliveryMode.regular,
                            system_preferences.preferred_language)
        self.assertEqual(member.address.email, 'aperson@example.com')
        self.assertEqual(member.list_id, 'test.example.com')
        self.assertEqual(member.role, MemberRole.member)

    def test_add_member_existing_user(self):
        # Test subscribing a user to a mailing list when the email address has
        # already been associated with a user.
        user_manager = getUtility(IUserManager)
        user_manager.create_user('aperson@example.com', 'Anne Person')
        member = add_member(self._mlist, 'aperson@example.com',
                            'Anne Person', '123', DeliveryMode.regular,
                            system_preferences.preferred_language)
        self.assertEqual(member.address.email, 'aperson@example.com')
        self.assertEqual(member.list_id, 'test.example.com')

    def test_add_member_banned(self):
        # Test that members who are banned by specific address cannot
        # subscribe to the mailing list.
        IBanManager(self._mlist).ban('anne@example.com')
        with self.assertRaises(MembershipIsBannedError) as cm:
            add_member(self._mlist, 'anne@example.com', 'Anne Person',
                       '123', DeliveryMode.regular,
                       system_preferences.preferred_language)
        self.assertEqual(
            str(cm.exception),
            'anne@example.com is not allowed to subscribe to test@example.com')

    def test_add_member_globally_banned(self):
        # Test that members who are banned by specific address cannot
        # subscribe to the mailing list.
        IBanManager(None).ban('anne@example.com')
        self.assertRaises(
            MembershipIsBannedError,
            add_member, self._mlist, 'anne@example.com', 'Anne Person',
            '123', DeliveryMode.regular, system_preferences.preferred_language)

    def test_add_member_banned_from_different_list(self):
        # Test that members who are banned by on a different list can still be
        # subscribed to other mlists.
        sample_list = create_list('sample@example.com')
        IBanManager(sample_list).ban('anne@example.com')
        member = add_member(self._mlist, 'anne@example.com',
                            'Anne Person', '123', DeliveryMode.regular,
                            system_preferences.preferred_language)
        self.assertEqual(member.address.email, 'anne@example.com')

    def test_add_member_banned_by_pattern(self):
        # Addresses matching regexp ban patterns cannot subscribe.
        IBanManager(self._mlist).ban('^.*@example.com')
        self.assertRaises(
            MembershipIsBannedError,
            add_member, self._mlist, 'anne@example.com', 'Anne Person',
            '123', DeliveryMode.regular, system_preferences.preferred_language)

    def test_add_member_globally_banned_by_pattern(self):
        # Addresses matching global regexp ban patterns cannot subscribe.
        IBanManager(None).ban('^.*@example.com')
        self.assertRaises(
            MembershipIsBannedError,
            add_member, self._mlist, 'anne@example.com', 'Anne Person',
            '123', DeliveryMode.regular, system_preferences.preferred_language)

    def test_add_member_banned_from_different_list_by_pattern(self):
        # Addresses matching regexp ban patterns on one list can still
        # subscribe to other mailing lists.
        sample_list = create_list('sample@example.com')
        IBanManager(sample_list).ban('^.*@example.com')
        member = add_member(self._mlist, 'anne@example.com',
                            'Anne Person', '123', DeliveryMode.regular,
                            system_preferences.preferred_language)
        self.assertEqual(member.address.email, 'anne@example.com')

    def test_add_member_moderator(self):
        # Test adding a moderator to a mailing list.
        member = add_member(self._mlist, 'aperson@example.com',
                            'Anne Person', '123', DeliveryMode.regular,
                            system_preferences.preferred_language,
                            MemberRole.moderator)
        self.assertEqual(member.address.email, 'aperson@example.com')
        self.assertEqual(member.list_id, 'test.example.com')
        self.assertEqual(member.role, MemberRole.moderator)

    def test_add_member_twice(self):
        # Adding a member with the same role twice causes an
        # AlreadySubscribedError to be raised.
        add_member(self._mlist, 'aperson@example.com',
                   'Anne Person', '123', DeliveryMode.regular,
                   system_preferences.preferred_language,
                   MemberRole.member)
        with self.assertRaises(AlreadySubscribedError) as cm:
            add_member(self._mlist, 'aperson@example.com',
                       'Anne Person', '123', DeliveryMode.regular,
                       system_preferences.preferred_language,
                       MemberRole.member)
        self.assertEqual(cm.exception.fqdn_listname, 'test@example.com')
        self.assertEqual(cm.exception.email, 'aperson@example.com')
        self.assertEqual(cm.exception.role, MemberRole.member)

    def test_add_member_with_different_roles(self):
        # Adding a member twice with different roles is okay.
        member_1 = add_member(self._mlist, 'aperson@example.com',
                              'Anne Person', '123', DeliveryMode.regular,
                              system_preferences.preferred_language,
                              MemberRole.member)
        member_2 = add_member(self._mlist, 'aperson@example.com',
                              'Anne Person', '123', DeliveryMode.regular,
                              system_preferences.preferred_language,
                              MemberRole.owner)
        self.assertEqual(member_1.list_id, member_2.list_id)
        self.assertEqual(member_1.address, member_2.address)
        self.assertEqual(member_1.user, member_2.user)
        self.assertNotEqual(member_1.member_id, member_2.member_id)
        self.assertEqual(member_1.role, MemberRole.member)
        self.assertEqual(member_2.role, MemberRole.owner)



class TestAddMemberPassword(unittest.TestCase):
    layer = ConfigLayer

    def setUp(self):
        self._mlist = create_list('test@example.com')

    def test_add_member_password(self):
        # Test that the password stored with the new user is encrypted.
        member = add_member(self._mlist, 'anne@example.com',
                            'Anne Person', 'abc', DeliveryMode.regular,
                            system_preferences.preferred_language)
        self.assertEqual(member.user.password, '{plaintext}abc')



class TestDeleteMember(unittest.TestCase):
    layer = ConfigLayer

    def setUp(self):
        self._mlist = create_list('test@example.com')

    def test_delete_member_not_a_member(self):
        # Try to delete an address which is not a member of the mailing list.
        with self.assertRaises(NotAMemberError) as cm:
            delete_member(self._mlist, 'noperson@example.com')
        self.assertEqual(
            str(cm.exception),
            'noperson@example.com is not a member of test@example.com')
