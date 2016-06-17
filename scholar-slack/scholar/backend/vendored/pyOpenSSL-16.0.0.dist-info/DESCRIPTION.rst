========================================================
pyOpenSSL -- A Python wrapper around the OpenSSL library
========================================================

.. image:: https://readthedocs.org/projects/pyopenssl/badge/?version=stable
   :target: https://pyopenssl.readthedocs.org/
   :alt: Stable Docs

.. image:: https://travis-ci.org/pyca/pyopenssl.svg?branch=master
   :target: https://travis-ci.org/pyca/pyopenssl
   :alt: Build status

.. image:: https://codecov.io/github/pyca/pyopenssl/coverage.svg?branch=master
   :target: https://codecov.io/github/pyca/pyopenssl
   :alt: Test coverage


High-level wrapper around a subset of the OpenSSL library.  Includes

* ``SSL.Connection`` objects, wrapping the methods of Python's portable sockets
* Callbacks written in Python
* Extensive error-handling mechanism, mirroring OpenSSL's error codes

... and much more.

You can find more information in the documentation_.
Development takes place on GitHub_.


Discussion
==========

If you run into bugs, you can file them in our `issue tracker`_.

We maintain a cryptography-dev_ mailing list for both user and development discussions.

You can also join ``#cryptography-dev`` on Freenode to ask questions or get involved.


.. _documentation: https://pyopenssl.readthedocs.org/
.. _`issue tracker`: https://github.com/pyca/pyopenssl/issues
.. _cryptography-dev: https://mail.python.org/mailman/listinfo/cryptography-dev
.. _GitHub: https://github.com/pyca/pyopenssl


Release Information
===================

16.0.0 (2016-03-19)
-------------------

This is the first release under full stewardship of PyCA.
We have made *many* changes to make local development more pleasing.
The test suite now passes both on Linux and OS X with OpenSSL 0.9.8, 1.0.1, and 1.0.2.
It has been moved to `py.test <https://pytest.org/>`_, all CI test runs are part of `tox <https://testrun.org/tox/>`_ and the source code has been made fully `flake8 <https://flake8.readthedocs.org/>`_ compliant.

We hope to have lowered the barrier for contributions significantly but are open to hear about any remaining frustrations.


Backward-incompatible changes:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Python 3.2 support has been dropped.
  It never had significant real world usage and has been dropped by our main dependency ``cryptography``.
  Affected users should upgrade to Python 3.3 or later.


Deprecations:
^^^^^^^^^^^^^

- The support for EGD has been removed.
  The only affected function ``OpenSSL.rand.egd()`` now uses ``os.urandom()`` to seed the internal PRNG instead.
  Please see `pyca/cryptography#1636 <https://github.com/pyca/cryptography/pull/1636>`_ for more background information on this decision.
  In accordance with our backward compatibility policy ``OpenSSL.rand.egd()`` will be *removed* no sooner than a year from the release of 16.0.0.

  Please note that you should `use urandom <http://sockpuppet.org/blog/2014/02/25/safely-generate-random-numbers/>`_ for all your secure random number needs.
- Python 2.6 support has been deprecated.
  Our main dependency ``cryptography`` deprecated 2.6 in version 0.9 (2015-05-14) with no time table for actually dropping it.
  pyOpenSSL will drop Python 2.6 support once ``cryptography`` does.


Changes:
^^^^^^^^

- Fixed ``OpenSSL.SSL.Context.set_session_id``, ``OpenSSL.SSL.Connection.renegotiate``, ``OpenSSL.SSL.Connection.renegotiate_pending``, and ``OpenSSL.SSL.Context.load_client_ca``.
  They were lacking an implementation since 0.14.
  `#422 <https://github.com/pyca/pyopenssl/pull/422>`_
- Fixed segmentation fault when using keys larger than 4096-bit to sign data.
  `#428 <https://github.com/pyca/pyopenssl/pull/428>`_
- Fixed ``AttributeError`` when ``OpenSSL.SSL.Connection.get_app_data()`` was called before setting any app data.
  `#304 <https://github.com/pyca/pyopenssl/pull/304>`_
- Added ``OpenSSL.crypto.dump_publickey()`` to dump ``OpenSSL.crypto.PKey`` objects that represent public keys, and ``OpenSSL.crypto.load_publickey()`` to load such objects from serialized representations.
  `#382 <https://github.com/pyca/pyopenssl/pull/382>`_
- Added ``OpenSSL.crypto.dump_crl()`` to dump a certificate revocation list out to a string buffer.
  `#368 <https://github.com/pyca/pyopenssl/pull/368>`_
- Added ``OpenSSL.SSL.Connection.get_state_string()`` using the OpenSSL binding ``state_string_long``.
  `#358 <https://github.com/pyca/pyopenssl/pull/358>`_
- Added support for the ``socket.MSG_PEEK`` flag to ``OpenSSL.SSL.Connection.recv()`` and ``OpenSSL.SSL.Connection.recv_into()``.
  `#294 <https://github.com/pyca/pyopenssl/pull/294>`_
- Added ``OpenSSL.SSL.Connection.get_protocol_version()`` and ``OpenSSL.SSL.Connection.get_protocol_version_name()``.
  `#244 <https://github.com/pyca/pyopenssl/pull/244>`_
- Switched to ``utf8string`` mask by default.
  OpenSSL formerly defaulted to a ``T61String`` if there were UTF-8 characters present.
  This was changed to default to ``UTF8String`` in the config around 2005, but the actual code didn't change it until late last year.
  This will default us to the setting that actually works.
  To revert this you can call ``OpenSSL.crypto._lib.ASN1_STRING_set_default_mask_asc(b"default")``.
  `#234 <https://github.com/pyca/pyopenssl/pull/234>`_

`Full changelog <https://pyopenssl.readthedocs.org/en/stable/changelog.html>`_.



