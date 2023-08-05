
=====
dy.fi
=====

dy.fi package provides script to keep dynamic IP address fresh for DNS service https://www.dy.fi provides.

Two commands
------------
Two commands will be added to buildout.

- ./bin/dyfi
- ./bin/dyfi-last-updated

Example of dyfi command::

    ./bin/dyfi -u USERACCOUNT -p PASSWORD hostname.com hostname.org

``USERACCOUNT`` and ``PASSWORD`` are same as what you use for https://www.dy.fi/ site log in.

You can pass multiple host names separated with a space,
here they are ``hostname.com`` and ``hostname.org``.

You can check the last updated time of IP address::

    ./bin/dyfi-last-updated

Changelog
---------


0.2 (2014-09-18)
================

- Use ipgetter to get your server global IP rather than from one server. [taito]

0.1 (2012-09-15)
================

- Initial release. [taito]
