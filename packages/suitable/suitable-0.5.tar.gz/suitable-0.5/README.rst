Suitable
========

Suitable is a thin wrapper around the Ansible API.

*Caution*
---------

.. DANGER::
    **This package is experimental, don't use in production.**

    **Suitable is not affiliated with Ansible and not supported by it.**

    **Use at your own risk.**

The endorsed way to use the official Ansible API is documented here:
http://docs.ansible.com/developing_api.html

Example
-------

.. code-block:: python

    from suitable import Api

    # creates the user 'denis' on both hosts
    hosts = Api(['web.seantis.dev', 'db.seantis.dev'])
    hosts.user(name='denis')

    # creates the user 'postgres' on db.seantis.dev
    dbhost = Api('dbhost.dev')
    dbhost.user(name='postgres')

    # returns a list of mounts on the given servers
    hosts.setup(filter='ansible_mounts')

    # connects to the given server with a specific user/pass
    from getpass import getpass
    username = 'admin'
    password = getpass()

    api = Api('web.seantis.dev', remote_user=username, remote_pass=password)
    print api.command('whoami').stdout('web.seantis.dev')

    >>> admin

Why Suitable?
-------------

Because 'ansible' is derived from 'answerable' whose archaic definitions
include 'suitable'. So not much thought went into it.

Are there tests, docs?
----------------------

Few tests, we use this so far for our internal deploy and server update scripts,
so the code is actually run in production if you will - but it's an experiment
because we've been using a number of ways to drive ansible within scripts
and we're not yet sure this is it. We'll add more over time as the interface
stabilizes.

No docs, there are a number of comments if you bother to read the source,
but there's no guide and no readthedocs page. If this module makes sense
to anyone else, we'll add more!

Run Tests
---------

.. code-block:: python

    pip install tox
    tox


More information
----------------

All the heavy lifting is done by Ansible. To get a list of Api arguments
have a look at the Runner class found in
https://github.com/ansible/ansible/blob/devel/lib/ansible/runner/__init__.py

To get an overview of all the methods provided by the api have a look at the
list of Ansible modules: http://docs.ansible.com/modules_by_category.html

The file module for instance includes the following example::

    - file: path=/etc/foo.conf owner=foo group=foo mode=0644

This can easily be translated to the suitable api::

    api.file(path='/etc/foo.conf', owner='foo', group='foo', mode='0644')

Changelog
---------

0.5 (2014-11-28)
~~~~~~~~~~~~~~~~

- Adds support for Ansible 1.8.
  [href]

- Includes automated tests for Ansible versions 1.5 through 1.8.
  [href]

- Properly escapes spaces in key-value pairs. Fixes #3.
  [href]

0.4 (2014-09-05)
~~~~~~~~~~~~~~~~

- Wraps the result of all module runs to provide easy access to results
  per server.
  [href]

- Default to transport 'localhost' if 'localhost' or '127.0.0.1' is used
  exclusively on the API object.
  [href]

0.3 (2014-05-28)
~~~~~~~~~~~~~~~~

- Adds a stern warning so users won't confuse this with the official Ansible API.
  [href]

0.2 (2014-05-21)
~~~~~~~~~~~~~~~~

- Change license to GPL v3 as required by Ansible.
  [href]

0.1 (2014-05-21)
~~~~~~~~~~~~~~~~

- Initial release.
  [href]
