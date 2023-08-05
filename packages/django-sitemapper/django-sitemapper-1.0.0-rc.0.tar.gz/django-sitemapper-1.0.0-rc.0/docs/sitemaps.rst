.. sitemap::

Setting up a sitemap
====================

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
