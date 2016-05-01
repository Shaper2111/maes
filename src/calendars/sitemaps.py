# -*- coding: utf-8 -*-
from datetime import date

from django.contrib.sitemaps import Sitemap
from psycopg2.extras import DateRange

from models import Archive, Calendar, Album


class ArchiveSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.5

    def items(self):
        return Archive.objects.all()


class ArchiveItemsSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.5

    def items(self):
        return Calendar.objects.filter(archive__isnull=False)

    def location(self, obj):
        return '/arhive/%d/%s/' % (obj.archive.year, obj.slug)


class CalendarSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Calendar.objects.filter(archive__isnull=True,
                                       dates__gte=DateRange(date.today(), date(date.today().year, 12, 31)))


class AlbumSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Album.objects.all()


calendars_sitemaps = {
    # 'archives': ArchiveSitemap,
    # 'archives-items': ArchiveItemsSitemap,
    # 'calendars': CalendarSitemap,
    # 'albums': AlbumSitemap,
}
