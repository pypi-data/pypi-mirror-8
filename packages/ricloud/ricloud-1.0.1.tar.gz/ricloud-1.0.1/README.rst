ricloud: iCloud access made easy
================================

This is a Python library for interaction with Reincubate's iCloud API. The Reincubate iCloud API provides powerful programmatic iCloud access to investigators, application developers and integrators. It is RESTful and makes many commonly-accessed forms of data available as JSON feeds.

The API includes functionality for extraction, manipulation and recovery of many types of iOS data, and has functionality to support bulk, scheduled, and realtime data access. 

Installation & usage
--------------------


The library can be installed with a single command:

.. code-block:: pycon

    $ pip install ricloud

A sample script is included which provides an example of how the API can be used to access a range of datatypes in a way that is compatible with Apple's 2FA mechanism.

.. code-block:: pycon

    $ python -c "from ricloud.sample_script import main; main();"

Configuration
~~~~~~~~~~~~~

The API relies on a set of security credentials, which are stored in an ``ricloud.ini`` file. This package ships with a default configuration file which enables limited access to the API for demonstration purposes. Full access can be gained by contacting enterprise@reincubate.com.

The default credentials can be overridden by creating an override file named ``.ricloud.ini`` in the running user's ``HOME`` directory. Alternately, an ``RICLOUD_CONF`` environment variable can be set, specifying the full path and filename of the configuration file.

This file should have the following details:

.. code-block:: ini

    [auth]
    # Required and supplied by Reincubate
    user = 
    key = 

    [test]
    # If you want to run automated tests against your account, set these.
    user =
    key =
    apple_id =
    password =

Need more functionality?
------------------------

Reincubate builds world class iOS and app data access and recovery technology. The company was founded in 2008 and was first to market with iOS backup extraction technology, consumer backup decryption, and more recently with enterprise iCloud support. Clients include law enforcement, government and security organisations in the US and internationally, and to corporations as large as Microsoft and IBM.

With six years' experience helping police forces, law firms and forensics labs access iOS data, the company can help enterprise users with:

* iCloud access and data recovery
* Recovery of data deleted from SQLite databases
* Bulk iOS data recovery
* Forensic examination of iOS data
* Passcode, password and keybag analysis
* Custom iOS app data extraction
* Advanced PList, TypedStream and Mbdb manipulation

Contact enterprise@reincubate.com for more information.

Users with simpler needs may wish to try the `iPhone Backup Extractor <http://www.iphonebackupextractor.com>`_, which provides a set of iCloud functionality better suited to consumers.

Terms & license
---------------

Users must not use the API in any way that is unlawful, illegal, fraudulent or harmful; or in connection with any unlawful, illegal, fraudulent or harmful purpose or activity. See the `LICENSE` file. Full terms are available from enterprise@reincubate.com.

Copyright Reincubate Ltd, 2014, all rights reserved.