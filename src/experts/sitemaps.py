# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap

from models import Client, Expert


class ClientSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Client.objects.all()


class ExpertSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Expert.objects.all()


experts_sitemaps = {
    'experts': ExpertSitemap,
}
