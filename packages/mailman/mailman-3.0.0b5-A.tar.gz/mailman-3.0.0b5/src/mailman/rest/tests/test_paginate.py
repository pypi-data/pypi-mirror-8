# Copyright (C) 2013-2014 by the Free Software Foundation, Inc.
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

"""paginate helper tests."""

from __future__ import absolute_import, print_function, unicode_literals

__metaclass__ = type
__all__ = [
    'TestPaginateHelper',
    ]


import unittest

from falcon import HTTPInvalidParam, Request
from mailman.app.lifecycle import create_list
from mailman.database.transaction import transaction
from mailman.rest.helpers import paginate
from mailman.testing.layers import RESTLayer



class _FakeRequest(Request):
    def __init__(self, count=None, page=None):
        self._params = {}
        if count is not None:
            self._params['count'] = count
        if page is not None:
            self._params['page'] = page



class TestPaginateHelper(unittest.TestCase):
    """Test the @paginate decorator."""

    layer = RESTLayer

    def setUp(self):
        with transaction():
            self._mlist = create_list('test@example.com')

    def test_no_pagination(self):
        # When there is no pagination params in the request, all 5 items in
        # the collection are returned.
        @paginate
        def get_collection(self, request):
            return ['one', 'two', 'three', 'four', 'five']
        # Expect 5 items
        page = get_collection(None, _FakeRequest())
        self.assertEqual(page, ['one', 'two', 'three', 'four', 'five'])

    def test_valid_pagination_request_page_one(self):
        # ?count=2&page=1 returns the first page, with two items in it.
        @paginate
        def get_collection(self, request):
            return ['one', 'two', 'three', 'four', 'five']
        page = get_collection(None, _FakeRequest(2, 1))
        self.assertEqual(page, ['one', 'two'])

    def test_valid_pagination_request_page_two(self):
        # ?count=2&page=2 returns the second page, where a page has two items
        # in it.
        @paginate
        def get_collection(self, request):
            return ['one', 'two', 'three', 'four', 'five']
        page = get_collection(None, _FakeRequest(2, 2))
        self.assertEqual(page, ['three', 'four'])

    def test_2nd_index_larger_than_total(self):
        # ?count=2&page=3 returns the third page with page size 2, but the
        # last page only has one item in it.
        @paginate
        def get_collection(self, request):
            return ['one', 'two', 'three', 'four', 'five']
        page = get_collection(None, _FakeRequest(2, 3))
        self.assertEqual(page, ['five'])

    def test_out_of_range_returns_empty_list(self):
        # ?count=2&page=4 returns the fourth page, which doesn't exist, so an
        # empty collection is returned.
        @paginate
        def get_collection(self, request):
            return ['one', 'two', 'three', 'four', 'five']
        page = get_collection(None, _FakeRequest(2, 4))
        self.assertEqual(page, [])

    def test_count_as_string_returns_bad_request(self):
        # ?count=two&page=2 are not valid values, so a bad request occurs.
        @paginate
        def get_collection(self, request):
            return []
        self.assertRaises(HTTPInvalidParam, get_collection,
                          None, _FakeRequest('two', 1))

    def test_negative_count(self):
        # ?count=-1&page=1
        @paginate
        def get_collection(self, request):
            return ['one', 'two', 'three', 'four', 'five']
        self.assertRaises(HTTPInvalidParam, get_collection,
                          None, _FakeRequest(-1, 1))

    def test_negative_page(self):
        # ?count=1&page=-1
        @paginate
        def get_collection(self, request):
            return ['one', 'two', 'three', 'four', 'five']
        self.assertRaises(HTTPInvalidParam, get_collection,
                          None, _FakeRequest(1, -1))

    def test_negative_page_and_count(self):
        # ?count=1&page=-1
        @paginate
        def get_collection(self, request):
            return ['one', 'two', 'three', 'four', 'five']
        self.assertRaises(HTTPInvalidParam, get_collection,
                          None, _FakeRequest(-1, -1))
