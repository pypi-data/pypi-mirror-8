devpi-ldap: LDAP authentication for devpi-server
================================================

For use with devpi-server >= 2.1.0.

Installation
------------

``devpi-ldap`` needs to be installed alongside ``devpi-server``.

You can install it with::

    pip install devpi-ldap

For ``devpi-server`` there is no configuration needed, as it will automatically discover the plugin through calling hooks using the setuptools entry points mechanism.

Details about LDAP configuration below.

Configuration
-------------

A script named ``devpi-ldap`` can be used to test your LDAP configuration.

To configure LDAP, create a yaml file with a dictionary containing another dictionary under the ``devpi-ldap`` key with the following options:

``url``
  The url of the LDAP server.
  Using ``ldaps://`` enables SSL.
  No certificate validation is performed at the moment.

``user_template``
  The template to generate the distinguished name for the user.
  If the structure is fixed, this is faster than specifying a ``user_search``, but ``devpi-server`` can't know whether a user exists or not.

``user_search``
  If you can't or don't want to use ``user_template``, then these are the search settings for the users distinguished name.
  You can use ``username`` in the search filter.
  See specifics below.

``group_search``
  The search settings for the group objects of the user.
  You can use ``username`` and ``userdn`` (the distinguished name) in the search filter.
  See specifics below.

``referrals``
  Whether to follow referrals.
  This needs to be set to ``false`` in many cases when using LDAP via Active Directory on Windows.
  The default is ``true``.

The ``user_search`` and ``group_search`` settings are dictionaries with the following options:

``base``
  The base location from which to search.

``filter``
  The search filter.
  To use replacements, put them in curly braces.
  Example: ``(&(objectClass=group)(member={userdn}))``

``scope``
  The scope for the search.
  Valid values are ``base-object``, ``single-level`` and ``whole-subtree``.
  The default is ``whole-subtree``.

``attribute_name``
  The name of the attribute which should be extracted from the search result.

``userdn``
  The distinguished name of the user which should be used for the search operation.
  If you don't have anonymous user search or if the users can't search their own groups, then you need to set this to a user which has the necessary rights.

``password``
  The password for the user in ``userdn``.

The YAML file should then look similar to this:

.. code-block:: yaml

    ---
    devpi-ldap:
      url: ldap://example.com
      user_template: CN={username},CN=Partition1,DC=Example,DC=COM
      group_search:
        base: CN=Partition1,DC=Example,DC=COM
        filter: (&(objectClass=group)(member={userdn}))
        attribute_name: CN

An example with user search and Active Directory might look like this:

.. code-block:: yaml

    ---
    devpi-ldap:
      url: ldap://example.com
      user_template: CN={username},CN=Partition1,DC=Example,DC=COM
      user_search:
        base: CN=Partition1,DC=Example,DC=COM
        filter: (&(objectClass=user)(sAMAccountName={username}))
        attribute_name: distinguishedName
      group_search:
        base: CN=Partition1,DC=Example,DC=COM
        filter: (&(objectClass=group)(member={userdn}))
        attribute_name: CN
