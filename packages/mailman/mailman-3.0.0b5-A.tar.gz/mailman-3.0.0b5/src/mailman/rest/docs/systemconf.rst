====================
System configuration
====================

The entire system configuration is available through the REST API.  You can
get a list of all defined sections.

    >>> dump_json('http://localhost:9001/3.0/system/configuration')
    http_etag: ...
    sections: ['antispam', 'archiver.mail_archive', 'archiver.master', ...

You can also get all the values for a particular section.

    >>> dump_json('http://localhost:9001/3.0/system/configuration/mailman')
    default_language: en
    email_commands_max_lines: 10
    filtered_messages_are_preservable: no
    http_etag: ...
    layout: testing
    noreply_address: noreply
    pending_request_life: 3d
    post_hook:
    pre_hook:
    sender_headers: from from_ reply-to sender
    site_owner: noreply@example.com

Dotted section names work too, for example, to get the French language
settings section.

    >>> dump_json('http://localhost:9001/3.0/system/configuration/language.fr')
    charset: iso-8859-1
    description: French
    enabled: yes
    http_etag: ...
