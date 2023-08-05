django-sitemapper
=================

A small Django app to manage sitemap.xml overrides on a per-object basis.

Brief installation notes are given below, but see our
`online documentation <http://django-sitemapper.readthedocs.org/en/latest/>`_
for more details.

.. image:: https://readthedocs.org/projects/django-sitemapper/badge/?version=latest
   :target: http://django-sitemapper.readthedocs.org/en/latest/
   :alt: Documentation Status



Requirements
------------

Django 1.4.2 or greater, Python 2.7 or greater.


Installation
------------

Use your favorite Python installer to install it from PyPI::

    $ pip install django-sitemapper

If you are using ``pip`` version 1.4 or later you'll need to explicitly allow pre-release installation::

    $ pip install --pre django-sitemapper

Or get the source from the application site::

    $ hg clone https://bitbucket.org/mhurt/django-sitemapper
    $ cd django-sitemapper
    $ python setup.py install


Configuration
-------------

Add ``"sitemapper"`` to your ``INSTALLED_APPS`` setting like this::

    INSTALLED_APPS = {
      ...
      'sitemapper'
    }

For Django 1.7 users, run ``python manage.py migrate`` to create the
models. Otherwise simply run ``python manage.py syncdb``.


Setting up a sitemap
--------------------

Create a ``sitemaps.py`` file within your app directory and add the following
(replacing MyModel with whatever you called yours)::

    # sitemaps.py
    from sitemapper.sitemaps import Sitemap
    from .models import MyModel


    class MyModelSitemap(Sitemap):

        # Set some defaults for your model's sitemap...
        default_changefreq = 'weekly'
        default_priority = 0.5

        # ... and the queryset you want to use...
        queryset = MyModel.objects.all()

        # ... and some means to access the last-modified timestamp.
        def lastmod(self, obj):
            return obj.lastmodified

From this point onwards you can use ``MyModelSitemap`` as you would any other
sitemaps instance. See
`Django's sitemaps documentation <https://docs.djangoproject.com/en/dev/ref/contrib/sitemaps/>`_
for how to wire this up with your urlconf.


Contribute
----------

- Issue Tracker: https://bitbucket.org/mhurt/django-sitemapper/issues
- Source Code: https://bitbucket.org/mhurt/django-sitemapper/


License
-------

The project is licensed under the MIT license.


Release Notes
-------------

1.0
~~~

- Fixed: Tests now run correctly on Django < 1.6 thanks to django-discover-runner.

- Improved tests.

- Added new content to docs/sitemaps covering basic usage steps.

Hurrah! Finally reached v1.0 :)


1.0.0-rc
~~~~~~~~

- Refactored: ``sitemapper.sitemaps`` has been refactored, with improved docstrings (i.e. I've written some).

- New: ``sitemapper.sitemaps.SitemapBase`` moves queryset and ContentType
  handling to a root class. The actual ``Sitemap`` class now extends this but
  is otherwise unchanged.

- New: ``sitemapper.sitemaps.GenericSitemap`` extends the ``Sitemap`` class but
  mirrors the signature of ``django.contrib.sitemaps.GenericSitemap``. The only
  difference is that passing ``priority`` or ``changefreq`` at initialisation
  only overrides the default fallbacks.


Please let me know if you have any questions, suggestions or problems to report
via the
`issue tracker <https://bitbucket.org/mhurt/django-sitemapper/issues>`_.



1.0.0-beta.3
~~~~~~~~~~~~

- **Deprecated**: ``sitemapper.mixins.Sitemap`` has moved; use ``sitemapper.sitemaps.Sitemap`` instead.

- Fixed: Incorrect tox testenv.

- Changed: Refactored ContentType lookup into custom manager method. ``Sitemap`` now uses ``SitemapEntry.get_for_model()`` method.



1.0.0-beta.2
~~~~~~~~~~~~

- **Schema**: ``SitemapEntry.priority`` and ``SitemapEntry.changefreq`` are now nullable.

- Fixed: admin select widget issue for SitemapEntry.priority values of decimal integers (i.e. '0.0' and '1.0')

- Changed: Refactored ``Sitemap.priority()`` and ``Sitemap.changefreq()`` methods.

- New: Added support for South migrations.

- New: Support Django 1.4.2 and greater.



1.0.0-beta.1
~~~~~~~~~~~~

- **Backwards Incompatible**: Removed ``sitemapper.SitemappedModel`` mixin. 

- Changed: ``sitemapper.mixins.Sitemap`` now handles all lookups internally, and more efficiently.

- New: Support Django 1.5 and greater.
