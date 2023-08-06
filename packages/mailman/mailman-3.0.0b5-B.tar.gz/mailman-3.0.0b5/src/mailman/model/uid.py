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

"""Unique IDs."""

__all__ = [
    'UID',
    ]



from mailman.database.model import Model
from mailman.database.transaction import dbconnection
from mailman.database.types import UUID
from sqlalchemy import Column, Integer



class UID(Model):
    """Enforce uniqueness of uids through a database table.

    This is used so that unique ids don't have to be tracked by each
    individual model object that uses them.  So for example, when a user is
    deleted, we don't have to keep separate track of its uid to prevent it
    from ever being used again.  This class, hooked up to the
    `UniqueIDFactory` serves that purpose.

    There is no interface for this class, because it's purely an internal
    implementation detail.
    """

    __tablename__ = 'uid'

    id = Column(Integer, primary_key=True)
    uid = Column(UUID, index=True)

    @dbconnection
    def __init__(self, store, uid):
        super(UID, self).__init__()
        self.uid = uid
        store.add(self)

    def __repr__(self):
        return '<UID {0} at {1}>'.format(self.uid, id(self))

    @staticmethod
    @dbconnection
    # Note that the parameter order is deliberate reversed here.  Normally,
    # `store` is the first parameter after `self`, but since this is a
    # staticmethod and there is no self, the decorator will see the uid in
    # arg[0].
    def record(uid, store):
        """Record the uid in the database.

        :param uid: The unique id.
        :type uid: unicode
        :raises ValueError: if the id is not unique.
        """
        existing = store.query(UID).filter_by(uid=uid)
        if existing.count() != 0:
            raise ValueError(uid)
        return UID(uid)
