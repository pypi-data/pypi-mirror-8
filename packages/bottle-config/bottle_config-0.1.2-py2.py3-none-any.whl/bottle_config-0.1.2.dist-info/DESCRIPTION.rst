Bottle Configuration
####################

.. _description:

Bottle Configuration -- Configure Bottle from files.

.. _badges:


.. image:: http://img.shields.io/travis/klen/bottle-config.svg?style=flat-square
    :target: http://travis-ci.org/klen/bottle-config
    :alt: Build Status

.. image:: http://img.shields.io/coveralls/klen/bottle-config.svg?style=flat-square
    :target: https://coveralls.io/r/klen/bottle-config
    :alt: Coverals

.. image:: http://img.shields.io/pypi/v/bottle-config.svg?style=flat-square
    :target: https://pypi.python.org/pypi/bottle-config
    :alt: Version

.. image:: http://img.shields.io/pypi/dm/bottle-config.svg?style=flat-square
    :target: https://pypi.python.org/pypi/bottle-config
    :alt: Downloads

.. image:: http://img.shields.io/gratipay/klen.svg?style=flat-square
    :target: https://www.gratipay.com/klen/
    :alt: Donate

.. _contents:

.. contents::

.. _requirements:

Requirements
=============

- python >= 2.6

.. _installation:

Installation
=============

**Bottle Configuration** should be installed using pip: ::

    pip install bottle_config

.. _usage:

Usage
=====

The application provide configuration like Django settings.

`settings.py`: ::

    DEBUG = True
    ANOTHER_OPTION = 'VALUE'


::

    import bottle
    from bottle_config import config

    app = bottle.Bottle()
    app.install(config)

    # See app.config

::

    import bottle
    from bottle_config import Config

    app = bottle.Bottle()
    app.install(Config('custom.default.module'))

    # See app.config

Use environment variable `BOTTLE_CONFIG` to set a configuration module

::

    BOTTLE_CONFIG=project.config.production python app.py

.. _bugtracker:

Bug tracker
===========

If you have any suggestions, bug reports or
annoyances please report them to the issue tracker
at https://github.com/klen/bottle_config/issues

.. _contributing:

Contributing
============

Development of starter happens at github: https://github.com/klen/bottle_config


Contributors
=============

* klen_ (Kirill Klenov)

.. _license:

License
=======

Licensed under a `BSD license`_.

.. _links:

.. _BSD license: http://www.linfo.org/bsdlicense.html
.. _klen: http://klen.github.com/


