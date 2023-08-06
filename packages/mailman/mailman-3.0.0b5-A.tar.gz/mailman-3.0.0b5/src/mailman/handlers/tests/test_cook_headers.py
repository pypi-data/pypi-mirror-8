# Copyright (C) 2014 by the Free Software Foundation, Inc.
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

"""Test the cook_headers handler."""

from __future__ import absolute_import, print_function, unicode_literals

__metaclass__ = type
__all__ = [
    'TestCookHeaders',
    ]


import unittest

from mailman.app.lifecycle import create_list
from mailman.handlers import cook_headers
from mailman.testing.helpers import get_queue_messages, make_digest_messages
from mailman.testing.layers import ConfigLayer



class TestCookHeaders(unittest.TestCase):
    """Test the cook_headers handler."""

    layer = ConfigLayer

    def setUp(self):
        self._mlist = create_list('test@example.com')

    def test_process_digest(self):
        # MIME digests messages are multiparts.
        make_digest_messages(self._mlist)
        messages = [bag.msg for bag in get_queue_messages('virgin')]
        self.assertEqual(len(messages), 2)
        for msg in messages:
            try:
                cook_headers.process(self._mlist, msg, {})
            except AttributeError as e:
                # LP: #1130696 would raise an AttributeError on .sender
                self.fail(e)
