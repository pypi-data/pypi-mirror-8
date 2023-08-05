from tendenci.core.rss.feedsmanager import SubFeed
from tendenci.core.site_settings.utils import get_setting
from tendenci.core.perms.utils import PUBLIC_FILTER
from tendenci.core.sitemaps import TendenciSitemap

from tendenci.apps.pages.models import Page

class LatestEntriesFeed(SubFeed):
    title =  '%s Latest Pages' % get_setting('site','global','sitedisplayname')
    link =  "/pages/"
    description =  "Latest Pages by %s" % get_setting('site','global','sitedisplayname')

    def items(self):
        items = Page.objects.filter(**PUBLIC_FILTER).filter(syndicate=True).order_by('-create_dt')[:20]
        return items

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_pubdate(self, item):
        return item.create_dt

    def item_link(self, item):
        return item.get_absolute_url()

class PageSitemap(TendenciSitemap):
    """ Sitemap information for pages """
    changefreq = "yearly"
    priority = 0.6

    def items(self):
        items = Page.objects.filter(**PUBLIC_FILTER).order_by('-create_dt')
        return items

    def lastmod(self, obj):
        return obj.update_dt
