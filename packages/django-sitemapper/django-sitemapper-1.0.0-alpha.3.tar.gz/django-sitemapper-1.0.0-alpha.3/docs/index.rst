.. django-sitemapper documentation master file, created by
   sphinx-quickstart on Sat Oct  4 22:39:45 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django-sitemapper's documentation!
=============================================


Sitemapper is a small Django app to manage sitemap.xml overrides on a
per-object basis.



Requirements
------------

Django 1.6 or greater, Python 2.7 or greater.



Installation
------------

Use your favorite Python installer to install it from PyPI::

    $ pip install django-sitemapper

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
    from sitemapper.mixins import Sitemap
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


.. toctree::
   :maxdepth: 2
   :hidden:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

