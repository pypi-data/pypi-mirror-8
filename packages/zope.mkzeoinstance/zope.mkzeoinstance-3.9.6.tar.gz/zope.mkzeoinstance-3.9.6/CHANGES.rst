Changelog
=========

3.9.6 (2014-12-23)
------------------

- Add support for testing on Travis, and with tox.


3.9.5 (2011-10-31)
------------------

- Place the socket used by the ``zeoctl`` control process to conmmunicate
  with its ``runzeo`` daemaon in ``$INSTANCE_HOME/var``, instead of
  ``$INSTANCE_HOME/etc`` (which would idealy not be writable by the process).
  See: https://bugs.launchpad.net/zope.mkzeoinstance/+bug/175981


3.9.4 (2010-04-22)
------------------

- Rename the script / package ``mkzeoinstance`` to avoid clashing with the
  script bundled with ZODB.

- Add an option to spell the host interface to be listened on, as well as
  the port the generated ZEO server configuration.  Thanks to Igor Stroh
  for the patch.  See: https://bugs.launchpad.net/zodb/+bug/143361

- Fix generated templates to cope with the move of ``zdaemon`` code into
  its own project.

- Fork from the version of the ``mkzeoinst`` script contained in
  ZODB 3.9.4.
