.. _install:

Installation
============

This part covers installing django-sitemapper and configuring your Django
project to use it.


Requirements
------------

Sitemapper currently requires Django 1.4.2 or greater and Python 2.7 or greater.

`South migrations <http://south.aeracode.org/>`_ are provided for Django
versions prior to 1.7, so if you'd like to use these please make sure you have
South installed before continuing.


Get the code
------------

Installing Sitemapper is simple with `pip <https//:pip.pypa.io>`_ (or, if you must, with `easy_install <http://pypi.python.org/pypi/setuptools>`_), just run this in your terminal::

    $ pip install django-sitemapper
    or
    $ easy_install django-sitemapper


Sitemapper is actively developed on Bitbucket, where you can grab 
`the latest code <https://bitbucket.org/mhurt/django-sitemapper>`_.

Either clone the repository::

    $ hg clone https://bitbucket.org/mhurt/django-sitemapper

or download and unpack the
`tar-ball or zip-ball of your choice <https://bitbucket.org/mhurt/django-sitemapper/downloads>`_.

Once you have a copy of the source, you can install it into
your site packages easily::

    $ cd django-sitemapper
    $ python setup.py install



Configuring your Django project
-------------------------------

Add ``"sitemapper"`` to your ``INSTALLED_APPS`` setting like this::

    INSTALLED_APPS = {
      ...
      'sitemapper'
    }

- For Django 1.7 users, run ``python manage.py migrate`` to create the
models.

- If you're using South, please see :ref:`withsouth`.

- Otherwise simply run ``python manage.py syncdb``.



.. _withsouth:

Using Sitemapper with South
---------------------------

If you're using Django 1.7 you won't need to use South as migrations are built in.

If you're using an earlier version of Django with South 1.0 the provided
south_migrations will be automatically detected.

For earlier versions of South you'll need to tell explicitly define which
migrations to use by adding to, or creating, the ``SOUTH_MIGRATION_MODULES`` in
your settings file::

    # settings.py
    ...
    SOUTH_MIGRATION_MODULES = {
        'sitemapper': 'sitemapper.south_migrations',
    }

Don't worry, though, as running running a ``migrate`` will complain loudly if
you've forgotten this step.
