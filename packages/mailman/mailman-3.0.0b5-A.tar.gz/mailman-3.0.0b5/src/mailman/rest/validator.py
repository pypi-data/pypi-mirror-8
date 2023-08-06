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

"""REST web form validation."""

from __future__ import absolute_import, print_function, unicode_literals

__metaclass__ = type
__all__ = [
    'PatchValidator',
    'Validator',
    'enum_validator',
    'language_validator',
    'subscriber_validator',
    ]


from uuid import UUID
from zope.component import getUtility

from mailman.core.errors import (
    ReadOnlyPATCHRequestError, UnknownPATCHRequestError)
from mailman.interfaces.languages import ILanguageManager


COMMASPACE = ', '



class enum_validator:
    """Convert an enum value name into an enum value."""

    def __init__(self, enum_class):
        self._enum_class = enum_class

    def __call__(self, enum_value):
        # This will raise a KeyError if the enum value is unknown.  The
        # Validator API requires turning this into a ValueError.
        try:
            return self._enum_class[enum_value]
        except KeyError as exception:
            # Retain the error message.
            raise ValueError(exception.args[0])


def subscriber_validator(subscriber):
    """Convert an email-or-int to an email-or-UUID."""
    try:
        return UUID(int=int(subscriber))
    except ValueError:
        return unicode(subscriber)


def language_validator(code):
    """Convert a language code to a Language object."""
    return getUtility(ILanguageManager)[code]



class Validator:
    """A validator of parameter input."""

    def __init__(self, **kws):
        if '_optional' in kws:
            self._optional = set(kws.pop('_optional'))
        else:
            self._optional = set()
        self._converters = kws.copy()

    def __call__(self, request):
        values = {}
        extras = set()
        cannot_convert = set()
        form_data = {}
        # All keys which show up only once in the form data get a scalar value
        # in the pre-converted dictionary.  All keys which show up more than
        # once get a list value.
        missing = object()
        items = request.params.items()
        for key, new_value in items:
            old_value = form_data.get(key, missing)
            if old_value is missing:
                form_data[key] = new_value
            elif isinstance(old_value, list):
                old_value.append(new_value)
            else:
                form_data[key] = [old_value, new_value]
        # Now do all the conversions.
        for key, value in form_data.items():
            try:
                values[key] = self._converters[key](value)
            except KeyError:
                extras.add(key)
            except (TypeError, ValueError):
                cannot_convert.add(key)
        # Make sure there are no unexpected values.
        if len(extras) != 0:
            extras = COMMASPACE.join(sorted(extras))
            raise ValueError('Unexpected parameters: {0}'.format(extras))
        # Make sure everything could be converted.
        if len(cannot_convert) != 0:
            bad = COMMASPACE.join(sorted(cannot_convert))
            raise ValueError('Cannot convert parameters: {0}'.format(bad))
        # Make sure nothing's missing.
        value_keys = set(values)
        required_keys = set(self._converters) - self._optional
        if value_keys & required_keys != required_keys:
            missing = COMMASPACE.join(sorted(required_keys - value_keys))
            raise ValueError('Missing parameters: {0}'.format(missing))
        return values

    def update(self, obj, request):
        """Update the object with the values in the request.

        This first validates and converts the attributes in the request, then
        updates the given object with the newly converted values.

        :param obj: The object to update.
        :type obj: object
        :param request: The HTTP request.
        :raises ValueError: if conversion failed for some attribute.
        """
        for key, value in self.__call__(request).items():
            self._converters[key].put(obj, key, value)



class PatchValidator(Validator):
    """Create a special validator for PATCH requests.

    PATCH is different than PUT because with the latter, you're changing the
    entire resource, so all expected attributes must exist.  With the former,
    you're only changing a subset of the attributes, so you only validate the
    ones that exist in the request.
    """
    def __init__(self, request, converters):
        """Create a validator for the PATCH request.

        :param request: The request object, which must have a .PATCH
            attribute.
        :param converters: A mapping of attribute names to the converter for
            that attribute's type.  Generally, this will be a GetterSetter
            instance, but it might be something more specific for custom data
            types (e.g. non-basic types like unicodes).
        :raises UnknownPATCHRequestError: if the request contains an unknown
            attribute, i.e. one that is not in the `attributes` mapping.
        :raises ReadOnlyPATCHRequest: if the requests contains an attribute
            that is defined as read-only.
        """
        validationators = {}
        for attribute in request.params:
            if attribute not in converters:
                raise UnknownPATCHRequestError(attribute)
            if converters[attribute].decoder is None:
                raise ReadOnlyPATCHRequestError(attribute)
            validationators[attribute] = converters[attribute]
        super(PatchValidator, self).__init__(**validationators)
