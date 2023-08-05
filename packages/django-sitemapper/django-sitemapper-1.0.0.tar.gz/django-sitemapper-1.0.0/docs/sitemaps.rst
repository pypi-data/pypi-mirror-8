.. sitemap:

Setting up a sitemap
====================

This section details all of the steps from a minimum working example, through
to a fully configured Sitemapper sitemap. In general this process is very
simple, and mirrors Django's own sitemaps, with only minor differences which
are explained below.


Getting Started
---------------

Create a ``sitemaps.py`` file within your app directory and add the following
(replacing MyModel with whatever you called yours)::

    # project/myapp/sitemaps.py
    from sitemapper.sitemaps import Sitemap
    from .models import MyModel


    class MyModelSitemap(Sitemap):

        # You'll need a queryset...
        queryset = MyModel.objects.all()

From this point onwards you can use ``MyModelSitemap`` as you would any other
sitemaps instance.

.. _basic urlconf:

In your root ``urls.py`` set up the sitemap as you would normally: ::

    # project/urls.py
    ...
    ...
    from django.contrib.sitemaps.views import sitemap
    from myapp.sitemaps import MyModelSitemap

    sitemaps = {
        'mymodel': MyModelSitemap,
        }

    urlpatterns = [
        # Your other patterns here
        ...
        ...

        url(r'^sitemap\.xml', sitemap, {'sitemaps': sitemaps},
            name='django.sitemaps.views.sitemap')

        ]


As you can see, the URL configuration is exactly the same as for Django's
built-in sitemaps. If you need more information on those see
`Django's sitemaps documentation <https://docs.djangoproject.com/en/dev/ref/contrib/sitemaps/>`_
for lots more details.


.. note:: 
   For this simplistic configuration the output of ``/sitemaps.xml`` will
   contain the ``<loc>`` URL for each object in your queryset.

   It will only show ``<changefreq>`` and ``<priority>`` if these have been
   assigned via a SitemapEntry.

   The ``<lastmod>`` field will not be displayed since we haven't, yet, defined
   how to find it.


Setting Defaults
----------------

So, lets make our sitemap a little more informative. We'll keep using our
`basic urlconf`_ for the moment::

    # project/myapp/sitemaps.py
    from sitemapper.sitemaps import Sitemap
    from .models import MyModel


    class MyModelSitemap(Sitemap):

        # You'll need a queryset...
        queryset = MyModel.objects.all()

        # Assign some sensible defaults...
        default_changefreq = 'weekly'
        default_priority = 0.5

Here we've defined two new attributes: ``default_changefreq`` and
``default_priority``. Like Django's own Sitemap class these, as you might
guess, allow you define the default values to use. But, unlike Django's Sitemap
class these will be overridden *if* a model instance has a ``changefreq`` or
``priority`` value assigned via a SitemapEntry.


.. caution::

   Make sure you don't accidentally override the ``changefreq`` or ``priority``
   attributes, as doing so will prevent that data being picked up from the
   SitemapEntry.


Getting the Timestamp
---------------------

The final stage of fully configuring our sitemap is to get the last-modfied date or time: ::

    # project/myapp/sitemaps.py
    from sitemapper.sitemaps import Sitemap
    from .models import MyModel


    class MyModelSitemap(Sitemap):

        # You'll need a queryset...
        queryset = MyModel.objects.all()

        # Assign some sensible defaults...
        default_changefreq = 'weekly'
        default_priority = 0.5

        # Get the date-/time-stamp
        def lastmod(self, item):
          return item.lastmodified


