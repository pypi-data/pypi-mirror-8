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

"""Web service helpers."""

__all__ = [
    'BadRequest',
    'ChildError',
    'GetterSetter',
    'NotFound',
    'bad_request',
    'child',
    'conflict',
    'created',
    'etag',
    'forbidden',
    'no_content',
    'not_found',
    'okay',
    'path_to',
    ]


import json
import falcon
import hashlib

from datetime import datetime, timedelta
from enum import Enum
from lazr.config import as_boolean
from mailman.config import config
from pprint import pformat



def path_to(resource):
    """Return the url path to a resource.

    :param resource: The canonical path to the resource, relative to the
        system base URI.
    :type resource: string
    :return: The full path to the resource.
    :rtype: bytes
    """
    return '{0}://{1}:{2}/{3}/{4}'.format(
        ('https' if as_boolean(config.webservice.use_https) else 'http'),
        config.webservice.hostname,
        config.webservice.port,
        config.webservice.api_version,
        (resource[1:] if resource.startswith('/') else resource),
        )



class ExtendedEncoder(json.JSONEncoder):
    """An extended JSON encoder which knows about other data types."""

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, timedelta):
            # as_timedelta() does not recognize microseconds, so convert these
            # to floating seconds, but only if there are any seconds.
            if obj.seconds > 0 or obj.microseconds > 0:
                seconds = obj.seconds + obj.microseconds / 1000000.0
                return '{0}d{1}s'.format(obj.days, seconds)
            return '{0}d'.format(obj.days)
        elif isinstance(obj, Enum):
            # It's up to the decoding validator to associate this name with
            # the right Enum class.
            return obj.name
        return json.JSONEncoder.default(self, obj)


def etag(resource):
    """Calculate the etag and return a JSON representation.

    The input is a dictionary representing the resource.  This
    dictionary must not contain an `http_etag` key.  This function
    calculates the etag by using the sha1 hexdigest of the
    pretty-printed (and thus key-sorted and predictable) representation
    of the dictionary.  It then inserts this value under the `http_etag`
    key, and returns the JSON representation of the modified dictionary.

    :param resource: The original resource representation.
    :type resource: dictionary
    :return: JSON representation of the modified dictionary.
    :rtype string
    """
    assert 'http_etag' not in resource, 'Resource already etagged'
    # Calculate the tag from a predictable (i.e. sorted) representation of the
    # dictionary.  The actual details aren't so important.  pformat() is
    # guaranteed to sort the keys, however it returns a str and the hash
    # library requires a bytes.  Use the safest possible encoding.
    hashfood = pformat(resource).encode('raw-unicode-escape')
    etag = hashlib.sha1(hashfood).hexdigest()
    resource['http_etag'] = '"{0}"'.format(etag)
    return json.dumps(resource, cls=ExtendedEncoder)


def paginate(method):
    """Method decorator to paginate through collection result lists.

    Use this to return only a slice of a collection, specified in the request
    itself.  The request should use query parameters `count` and `page` to
    specify the slice they want.  The slice will start at index
    ``(page - 1) * count`` and end (exclusive) at ``(page * count)``.

    Decorated methods must take ``self`` and ``request`` as the first two
    arguments.
    """
    def wrapper(self, request, *args, **kwargs):
        # Allow falcon's HTTPBadRequest exceptions to percolate up.  They'll
        # get turned into HTTP 400 errors.
        count = request.get_param_as_int('count', min=0)
        page = request.get_param_as_int('page', min=1)
        result = method(self, request, *args, **kwargs)
        if count is None and page is None:
            return result
        list_start = (page - 1) * count
        list_end = page * count
        return result[list_start:list_end]
    return wrapper



class CollectionMixin:
    """Mixin class for common collection-ish things."""

    def _resource_as_dict(self, resource):
        """Return the dictionary representation of a resource.

        This must be implemented by subclasses.

        :param resource: The resource object.
        :type resource: object
        :return: The representation of the resource.
        :rtype: dict
        """
        raise NotImplementedError

    def _resource_as_json(self, resource):
        """Return the JSON formatted representation of the resource."""
        return etag(self._resource_as_dict(resource))

    def _get_collection(self, request):
        """Return the collection as a concrete list.

        This must be implemented by subclasses.

        :param request: An http request.
        :return: The collection
        :rtype: list
        """
        raise NotImplementedError

    def _make_collection(self, request):
        """Provide the collection to the REST layer."""
        collection = self._get_collection(request)
        if len(collection) == 0:
            return dict(start=0, total_size=0)
        else:
            entries = [self._resource_as_dict(resource)
                       for resource in collection]
            # Tag the resources but use the dictionaries.
            [etag(resource) for resource in entries]
            # Create the collection resource
            return dict(
                start=0,
                total_size=len(collection),
                entries=entries,
                )



class GetterSetter:
    """Get and set attributes on an object.

    Most attributes are fairly simple - a getattr() or setattr() on the object
    does the trick, with the appropriate encoding or decoding on the way in
    and out.  Encoding doesn't happen here though; the standard JSON library
    handles most types, but see ExtendedEncoder for additional support.

    Others are more complicated since they aren't kept in the model as direct
    columns in the database.  These will use subclasses of this base class.
    Read-only attributes will have a decoder which always raises ValueError.
    """

    def __init__(self, decoder=None):
        """Create a getter/setter for a specific attribute.

        :param decoder: The callable for decoding a web request value string
            into the specific data type needed by the object's attribute.  Use
            None to indicate a read-only attribute.  The callable should raise
            ValueError when the web request value cannot be converted.
        :type decoder: callable
        """
        self.decoder = decoder

    def get(self, obj, attribute):
        """Return the named object attribute value.

        :param obj: The object to access.
        :type obj: object
        :param attribute: The attribute name.
        :type attribute: string
        :return: The attribute value, ready for JSON encoding.
        :rtype: object
        """
        return getattr(obj, attribute)

    def put(self, obj, attribute, value):
        """Set the named object attribute value.

        :param obj: The object to change.
        :type obj: object
        :param attribute: The attribute name.
        :type attribute: string
        :param value: The new value for the attribute.
        """
        setattr(obj, attribute, value)

    def __call__(self, value):
        """Convert the value to its internal format.

        :param value: The web request value to convert.
        :type value: string
        :return: The converted value.
        :rtype: object
        """
        if self.decoder is None:
            return value
        return self.decoder(value)



# Falcon REST framework add-ons.

def child(matcher=None):
    def decorator(func):
        if matcher is None:
            func.__matcher__ = func.__name__
        else:
            func.__matcher__ = matcher
        return func
    return decorator


class ChildError:
    def __init__(self, status):
        self._status = status

    def _oops(self, request, response):
        raise falcon.HTTPError(self._status, None)

    on_get = _oops
    on_post = _oops
    on_put = _oops
    on_patch = _oops
    on_delete = _oops


class BadRequest(ChildError):
    def __init__(self):
        super(BadRequest, self).__init__(falcon.HTTP_400)


class NotFound(ChildError):
    def __init__(self):
        super(NotFound, self).__init__(falcon.HTTP_404)


def okay(response, body=None):
    response.status = falcon.HTTP_200
    if body is not None:
        response.body = body


def no_content(response):
    response.status = falcon.HTTP_204


def not_found(response, body=b'404 Not Found'):
    response.status = falcon.HTTP_404
    if body is not None:
        response.body = body


def bad_request(response, body='400 Bad Request'):
    response.status = falcon.HTTP_400
    if body is not None:
        response.body = body


def created(response, location):
    response.status = falcon.HTTP_201
    response.location = location


def conflict(response, body=b'409 Conflict'):
    response.status = falcon.HTTP_409
    if body is not None:
        response.body = body


def forbidden(response, body=b'403 Forbidden'):
    response.status = falcon.HTTP_403
    if body is not None:
        response.body = body
