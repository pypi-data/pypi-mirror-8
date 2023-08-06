# Copyright (C) 2006-2014 by the Free Software Foundation, Inc.
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

"""Model for addresses."""

from __future__ import absolute_import, print_function, unicode_literals

__metaclass__ = type
__all__ = [
    'Address',
    ]


from email.utils import formataddr
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Unicode
from sqlalchemy.orm import relationship, backref
from zope.component import getUtility
from zope.event import notify
from zope.interface import implementer

from mailman.database.model import Model
from mailman.interfaces.address import (
    AddressVerificationEvent, IAddress, IEmailValidator)
from mailman.utilities.datetime import now



@implementer(IAddress)
class Address(Model):
    """See `IAddress`."""

    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    email = Column(Unicode)
    _original = Column(Unicode)
    display_name = Column(Unicode)
    _verified_on = Column('verified_on', DateTime)
    registered_on = Column(DateTime)

    user_id = Column(Integer, ForeignKey('user.id'), index=True)

    preferences_id = Column(Integer, ForeignKey('preferences.id'), index=True)
    preferences = relationship(
        'Preferences', backref=backref('address', uselist=False))

    def __init__(self, email, display_name):
        super(Address, self).__init__()
        getUtility(IEmailValidator).validate(email)
        lower_case = email.lower()
        self.email = lower_case
        self.display_name = display_name
        self._original = (None if lower_case == email else email)
        self.registered_on = now()

    def __str__(self):
        addr = (self.email if self._original is None else self._original)
        return formataddr((self.display_name, addr))

    def __repr__(self):
        verified = ('verified' if self.verified_on else 'not verified')
        address_str = str(self)
        if self._original is None:
            return '<Address: {0} [{1}] at {2:#x}>'.format(
                address_str, verified, id(self))
        else:
            return '<Address: {0} [{1}] key: {2} at {3:#x}>'.format(
                address_str, verified, self.email, id(self))

    @property
    def verified_on(self):
        return self._verified_on

    @verified_on.setter
    def verified_on(self, timestamp):
        self._verified_on = timestamp
        notify(AddressVerificationEvent(self))

    @property
    def original_email(self):
        return (self.email if self._original is None else self._original)
