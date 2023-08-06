# Copyright (C) 2010-2014 by the Free Software Foundation, Inc.
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

"""REST for members."""

__all__ = [
    'AMember',
    'AllMembers',
    'FindMembers',
    'MemberCollection',
    ]


import six

from mailman.app.membership import delete_member
from mailman.interfaces.address import InvalidEmailAddressError
from mailman.interfaces.listmanager import IListManager, NoSuchListError
from mailman.interfaces.member import (
    AlreadySubscribedError, DeliveryMode, MemberRole, MembershipError,
    NotAMemberError)
from mailman.interfaces.subscriptions import ISubscriptionService
from mailman.interfaces.user import UnverifiedAddressError
from mailman.interfaces.usermanager import IUserManager
from mailman.rest.helpers import (
    CollectionMixin, NotFound, bad_request, child, conflict, created, etag,
    no_content, not_found, okay, paginate, path_to)
from mailman.rest.preferences import Preferences, ReadOnlyPreferences
from mailman.rest.validator import (
    Validator, enum_validator, subscriber_validator)
from operator import attrgetter
from uuid import UUID
from zope.component import getUtility



class _MemberBase(CollectionMixin):
    """Shared base class for member representations."""

    def _resource_as_dict(self, member):
        """See `CollectionMixin`."""
        enum, dot, role = str(member.role).partition('.')
        # The member will always have a member id and an address id.  It will
        # only have a user id if the address is linked to a user.
        # E.g. nonmembers we've only seen via postings to lists they are not
        # subscribed to will not have a user id.   The user_id and the
        # member_id are UUIDs.  We need to use the integer equivalent in the
        # URL.
        response = dict(
            list_id=member.list_id,
            email=member.address.email,
            role=role,
            address=path_to('addresses/{}'.format(member.address.email)),
            self_link=path_to('members/{}'.format(member.member_id.int)),
            delivery_mode=member.delivery_mode,
            )
        # Add the user link if there is one.
        user = member.user
        if user is not None:
            response['user'] = path_to('users/{}'.format(user.user_id.int))
        return response

    @paginate
    def _get_collection(self, request):
        """See `CollectionMixin`."""
        return list(getUtility(ISubscriptionService))



class MemberCollection(_MemberBase):
    """Abstract class for supporting submemberships.

    This is used for example to return a resource representing all the
    memberships of a mailing list, or all memberships for a specific email
    address.
    """
    def _get_collection(self, request):
        """See `CollectionMixin`."""
        raise NotImplementedError

    def on_get(self, request, response):
        """roster/[members|owners|moderators]"""
        resource = self._make_collection(request)
        okay(response, etag(resource))



class AMember(_MemberBase):
    """A member."""

    def __init__(self, member_id_string):
        # REST gives us the member id as the string of an int; we have to
        # convert it to a UUID.
        try:
            member_id = UUID(int=int(member_id_string))
        except ValueError:
            # The string argument could not be converted to an integer.
            self._member = None
        else:
            service = getUtility(ISubscriptionService)
            self._member = service.get_member(member_id)

    def on_get(self, request, response):
        """Return a single member end-point."""
        if self._member is None:
            not_found(response)
        else:
            okay(response, self._resource_as_json(self._member))

    @child()
    def preferences(self, request, segments):
        """/members/<id>/preferences"""
        if len(segments) != 0:
            return NotFound(), []
        if self._member is None:
            return NotFound(), []
        child = Preferences(
            self._member.preferences,
            'members/{0}'.format(self._member.member_id.int))
        return child, []

    @child()
    def all(self, request, segments):
        """/members/<id>/all/preferences"""
        if len(segments) == 0:
            return NotFound(), []
        if self._member is None:
            return NotFound(), []
        child = ReadOnlyPreferences(
            self._member,
            'members/{0}/all'.format(self._member.member_id.int))
        return child, []

    def on_delete(self, request, response):
        """Delete the member (i.e. unsubscribe)."""
        # Leaving a list is a bit different than deleting a moderator or
        # owner.  Handle the former case first.  For now too, we will not send
        # an admin or user notification.
        if self._member is None:
            not_found(response)
            return
        mlist = getUtility(IListManager).get_by_list_id(self._member.list_id)
        if self._member.role is MemberRole.member:
            try:
                delete_member(mlist, self._member.address.email, False, False)
            except NotAMemberError:
                not_found(response)
                return
        else:
            self._member.unsubscribe()
        no_content(response)

    def on_patch(self, request, response):
        """Patch the membership.

        This is how subscription changes are done.
        """
        if self._member is None:
            not_found(response)
            return
        try:
            values = Validator(
                address=six.text_type,
                delivery_mode=enum_validator(DeliveryMode),
                _optional=('address', 'delivery_mode'))(request)
        except ValueError as error:
            bad_request(response, str(error))
            return
        if 'address' in values:
            email = values['address']
            address = getUtility(IUserManager).get_address(email)
            if address is None:
                bad_request(response, b'Address not registered')
                return
            try:
                self._member.address = address
            except (MembershipError, UnverifiedAddressError) as error:
                bad_request(response, str(error))
                return
        if 'delivery_mode' in values:
            self._member.preferences.delivery_mode = values['delivery_mode']
        no_content(response)



class AllMembers(_MemberBase):
    """The members."""

    def on_post(self, request, response):
        """Create a new member."""
        service = getUtility(ISubscriptionService)
        try:
            validator = Validator(
                list_id=six.text_type,
                subscriber=subscriber_validator,
                display_name=six.text_type,
                delivery_mode=enum_validator(DeliveryMode),
                role=enum_validator(MemberRole),
                _optional=('delivery_mode', 'display_name', 'role'))
            member = service.join(**validator(request))
        except AlreadySubscribedError:
            conflict(response, b'Member already subscribed')
        except NoSuchListError:
            bad_request(response, b'No such list')
        except InvalidEmailAddressError:
            bad_request(response, b'Invalid email address')
        except ValueError as error:
            bad_request(response, str(error))
        else:
            # The member_id are UUIDs.  We need to use the integer equivalent
            # in the URL.
            member_id = member.member_id.int
            location = path_to('members/{0}'.format(member_id))
            created(response, location)

    def on_get(self, request, response):
        """/members"""
        resource = self._make_collection(request)
        okay(response, etag(resource))



class _FoundMembers(MemberCollection):
    """The found members collection."""

    def __init__(self, members):
        super(_FoundMembers, self).__init__()
        self._members = members

    def _get_collection(self, request):
        """See `CollectionMixin`."""
        address_of_member = attrgetter('address.email')
        return list(sorted(self._members, key=address_of_member))


class FindMembers(_MemberBase):
    """/members/find"""

    def on_post(self, request, response):
        """Find a member"""
        service = getUtility(ISubscriptionService)
        validator = Validator(
            list_id=six.text_type,
            subscriber=six.text_type,
            role=enum_validator(MemberRole),
            _optional=('list_id', 'subscriber', 'role'))
        try:
            members = service.find_members(**validator(request))
        except ValueError as error:
            bad_request(response, str(error))
        else:
            resource = _FoundMembers(members)._make_collection(request)
            okay(response, etag(resource))
