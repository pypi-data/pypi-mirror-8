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

"""Mailing list configuration via REST API."""

__all__ = [
    'ListConfiguration',
    ]


import six

from lazr.config import as_boolean, as_timedelta
from mailman.config import config
from mailman.core.errors import (
    ReadOnlyPATCHRequestError, UnknownPATCHRequestError)
from mailman.interfaces.action import Action
from mailman.interfaces.archiver import ArchivePolicy
from mailman.interfaces.autorespond import ResponseAction
from mailman.interfaces.mailinglist import IAcceptableAliasSet, ReplyToMunging
from mailman.rest.helpers import (
    GetterSetter, bad_request, etag, no_content, okay)
from mailman.rest.validator import PatchValidator, Validator, enum_validator



class AcceptableAliases(GetterSetter):
    """Resource for the acceptable aliases of a mailing list."""

    def get(self, mlist, attribute):
        """Return the mailing list's acceptable aliases."""
        assert attribute == 'acceptable_aliases', (
            'Unexpected attribute: {}'.format(attribute))
        aliases = IAcceptableAliasSet(mlist)
        return sorted(aliases.aliases)

    def put(self, mlist, attribute, value):
        """Change the acceptable aliases.

        Because this is a PUT operation, all previous aliases are cleared
        first.  Thus, this is an overwrite.  The keys in the request are
        ignored.
        """
        assert attribute == 'acceptable_aliases', (
            'Unexpected attribute: {}'.format(attribute))
        alias_set = IAcceptableAliasSet(mlist)
        alias_set.clear()
        for alias in value:
            alias_set.add(alias)



# Additional validators for converting from web request strings to internal
# data types.  See below for details.

def pipeline_validator(pipeline_name):
    """Convert the pipeline name to a string, but only if it's known."""
    if pipeline_name in config.pipelines:
        return pipeline_name
    raise ValueError('Unknown pipeline: {}'.format(pipeline_name))


def list_of_str(values):
    """Turn a list of things into a list of unicodes."""
    for value in values:
        if not isinstance(value, str):
            raise ValueError('Expected str, got {!r}'.format(value))
    return values



# This is the list of IMailingList attributes that are exposed through the
# REST API.  The values of the keys are the GetterSetter instance holding the
# decoder used to convert the web request string to an internally valid value.
# The instance also contains the get() and put() methods used to retrieve and
# set the attribute values.  Its .decoder attribute will be None for read-only
# attributes.
#
# The decoder must either return the internal value or raise a ValueError if
# the conversion failed (e.g. trying to turn 'Nope' into a boolean).
#
# Many internal value types can be automatically JSON encoded, but see
# mailman.rest.helpers.ExtendedEncoder for specializations of certain types
# (e.g. datetimes, timedeltas, enums).

ATTRIBUTES = dict(
    acceptable_aliases=AcceptableAliases(list_of_str),
    admin_immed_notify=GetterSetter(as_boolean),
    admin_notify_mchanges=GetterSetter(as_boolean),
    administrivia=GetterSetter(as_boolean),
    advertised=GetterSetter(as_boolean),
    anonymous_list=GetterSetter(as_boolean),
    autorespond_owner=GetterSetter(enum_validator(ResponseAction)),
    autorespond_postings=GetterSetter(enum_validator(ResponseAction)),
    autorespond_requests=GetterSetter(enum_validator(ResponseAction)),
    autoresponse_grace_period=GetterSetter(as_timedelta),
    autoresponse_owner_text=GetterSetter(six.text_type),
    autoresponse_postings_text=GetterSetter(six.text_type),
    autoresponse_request_text=GetterSetter(six.text_type),
    archive_policy=GetterSetter(enum_validator(ArchivePolicy)),
    bounces_address=GetterSetter(None),
    collapse_alternatives=GetterSetter(as_boolean),
    convert_html_to_plaintext=GetterSetter(as_boolean),
    created_at=GetterSetter(None),
    default_member_action=GetterSetter(enum_validator(Action)),
    default_nonmember_action=GetterSetter(enum_validator(Action)),
    description=GetterSetter(six.text_type),
    digest_last_sent_at=GetterSetter(None),
    digest_size_threshold=GetterSetter(float),
    filter_content=GetterSetter(as_boolean),
    first_strip_reply_to=GetterSetter(as_boolean),
    fqdn_listname=GetterSetter(None),
    mail_host=GetterSetter(None),
    allow_list_posts=GetterSetter(as_boolean),
    include_rfc2369_headers=GetterSetter(as_boolean),
    join_address=GetterSetter(None),
    last_post_at=GetterSetter(None),
    leave_address=GetterSetter(None),
    list_name=GetterSetter(None),
    next_digest_number=GetterSetter(None),
    no_reply_address=GetterSetter(None),
    owner_address=GetterSetter(None),
    post_id=GetterSetter(None),
    posting_address=GetterSetter(None),
    posting_pipeline=GetterSetter(pipeline_validator),
    display_name=GetterSetter(six.text_type),
    reply_goes_to_list=GetterSetter(enum_validator(ReplyToMunging)),
    reply_to_address=GetterSetter(six.text_type),
    request_address=GetterSetter(None),
    scheme=GetterSetter(None),
    send_welcome_message=GetterSetter(as_boolean),
    subject_prefix=GetterSetter(six.text_type),
    volume=GetterSetter(None),
    web_host=GetterSetter(None),
    welcome_message_uri=GetterSetter(six.text_type),
    )


VALIDATORS = ATTRIBUTES.copy()
for attribute, gettersetter in list(VALIDATORS.items()):
    if gettersetter.decoder is None:
        del VALIDATORS[attribute]



class ListConfiguration:
    """A mailing list configuration resource."""

    def __init__(self, mailing_list, attribute):
        self._mlist = mailing_list
        self._attribute = attribute

    def on_get(self, request, response):
        """Get a mailing list configuration."""
        resource = {}
        if self._attribute is None:
            # Return all readable attributes.
            for attribute in ATTRIBUTES:
                value = ATTRIBUTES[attribute].get(self._mlist, attribute)
                resource[attribute] = value
        elif self._attribute not in ATTRIBUTES:
            bad_request(
                response, b'Unknown attribute: {}'.format(self._attribute))
            return
        else:
            attribute = self._attribute
            value = ATTRIBUTES[attribute].get(self._mlist, attribute)
            resource[attribute] = value
        okay(response, etag(resource))

    def on_put(self, request, response):
        """Set a mailing list configuration."""
        attribute = self._attribute
        if attribute is None:
            validator = Validator(**VALIDATORS)
            try:
                validator.update(self._mlist, request)
            except ValueError as error:
                bad_request(response, str(error))
                return
        elif attribute not in ATTRIBUTES:
            bad_request(response, b'Unknown attribute: {}'.format(attribute))
            return
        elif ATTRIBUTES[attribute].decoder is None:
            bad_request(
                response, b'Read-only attribute: {}'.format(attribute))
            return
        else:
            validator = Validator(**{attribute: VALIDATORS[attribute]})
            try:
                validator.update(self._mlist, request)
            except ValueError as error:
                bad_request(response, str(error))
                return
        no_content(response)

    def on_patch(self, request, response):
        """Patch the configuration (i.e. partial update)."""
        try:
            validator = PatchValidator(request, ATTRIBUTES)
        except UnknownPATCHRequestError as error:
            bad_request(
                response, b'Unknown attribute: {}'.format(error.attribute))
            return
        except ReadOnlyPATCHRequestError as error:
            bad_request(
                response, b'Read-only attribute: {}'.format(error.attribute))
            return
        try:
            validator.update(self._mlist, request)
        except ValueError as error:
            bad_request(response, str(error))
        else:
            no_content(response)
