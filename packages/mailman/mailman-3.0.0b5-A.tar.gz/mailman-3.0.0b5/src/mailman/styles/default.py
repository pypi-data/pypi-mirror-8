# Copyright (C) 2007-2014 by the Free Software Foundation, Inc.
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

"""Application of list styles to new and existing lists."""

from __future__ import absolute_import, print_function, unicode_literals

__metaclass__ = type
__all__ = [
    'LegacyDefaultStyle',
    'LegacyAnnounceOnly',
    ]


from zope.interface import implementer

from mailman.interfaces.styles import IStyle
from mailman.styles.base import (
    Announcement, BasicOperation, Bounces, Discussion, Identity, Moderation,
    Public)



@implementer(IStyle)
class LegacyDefaultStyle(
        Identity, BasicOperation, Bounces, Public, Discussion, Moderation):

    """The legacy default style."""

    name = 'legacy-default'

    def apply(self, mailing_list):
        """See `IStyle`."""
        Identity.apply(self, mailing_list)
        BasicOperation.apply(self, mailing_list)
        Bounces.apply(self, mailing_list)
        Public.apply(self, mailing_list)
        Discussion.apply(self, mailing_list)
        Moderation.apply(self, mailing_list)


@implementer(IStyle)
class LegacyAnnounceOnly(
        Identity, BasicOperation, Bounces, Public, Announcement, Moderation):

    """Similar to the legacy-default style, but for announce-only lists."""

    name = 'legacy-announce'

    def apply(self, mailing_list):
        """See `IStyle`."""
        Identity.apply(self, mailing_list)
        BasicOperation.apply(self, mailing_list)
        Bounces.apply(self, mailing_list)
        Public.apply(self, mailing_list)
        Announcement.apply(self, mailing_list)
        Moderation.apply(self, mailing_list)
