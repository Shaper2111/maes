# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap

from models import News, Post


class NewsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return News.objects.all()


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Post.objects.all()


blog_sitemaps = {
    'news': NewsSitemap,
    'posts': PostSitemap,
}
