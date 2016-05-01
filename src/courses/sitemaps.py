# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap

from models import Act, Competence, Training, Teaching, Solution, Rising, Event, Comment


class ActSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Act.objects.all()


class CompetenceSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Competence.objects.all()

    def location(self, obj):
        return '/competences/%d/teachings' % obj.id


class TrainingSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Training.objects.all()


class TeachingSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Teaching.objects.all()


class SolutionSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Solution.objects.all()


class RisingSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Rising.objects.all()


class EventSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Event.objects.all()


class CommentSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Comment.objects.all()


courses_sitemaps = {
    # 'acts': ActSitemap,
    'competences': CompetenceSitemap,
    'trainings': TrainingSitemap,
    'teachings': TeachingSitemap,
    'solutions': SolutionSitemap,
    'rising': RisingSitemap,
    'event': EventSitemap,
}
