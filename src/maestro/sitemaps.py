# -*- coding: utf-8 -*-
from blog.sitemaps import blog_sitemaps
from calendars.sitemaps import calendars_sitemaps
from courses.sitemaps import courses_sitemaps
from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from experts.sitemaps import experts_sitemaps


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['home', 'news', 'stats', 'trainers', 'company', 'feedback', 'photo']

    def location(self, item):
        return reverse(item, urlconf='maestro.ajax_urls')


sitemaps = {
    'static': StaticViewSitemap,
}
sitemaps.update(blog_sitemaps)
sitemaps.update(calendars_sitemaps)
sitemaps.update(courses_sitemaps)
sitemaps.update(experts_sitemaps)
