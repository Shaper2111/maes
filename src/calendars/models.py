# -*- coding: utf-8 -*-
from datetime import date

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import DateRangeField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from psycopg2.extras import DateRange


class Archive(models.Model):
    year = models.IntegerField(_(u'Год'), blank=False, null=True, unique=True)

    def __unicode__(self):
        return str(self.year)

    def get_absolute_url(self):
        return '/arhive/%d' % self.year

    class Meta:
        ordering = ['year']
        verbose_name = _(u'Архив')
        verbose_name_plural = _(u'Архивы')


class CalendarManager(models.Manager):
    def future_courses(self):
        return self.filter(archive__isnull=True,
                           dates__gte=DateRange(date.today(), date(date.today().year, 12, 31))).order_by('dates')


class Calendar(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    slug = models.SlugField(_(u'Путь в адресной строке'), blank=False, unique=True, max_length=300)
    dates = DateRangeField(_(u'Даты проведения'), blank=True, null=True)
    year = models.IntegerField(_(u'Год'), blank=True, null=True)
    archive = models.ForeignKey(Archive, verbose_name=_(u'Архив'), blank=True, null=True)
    objects = CalendarManager()

    def get_absolute_url(self):
        return '/training-calendar/%s' % self.slug

    class Meta:
        ordering = ['slug']
        verbose_name = _(u'Календарь')
        verbose_name_plural = _(u'Календари')


class Album(models.Model):
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    name = models.CharField(_(u'Название'), null=True, max_length=300)
    slug = models.SlugField(_(u'Путь в адресной строке'), blank=False, unique=True, max_length=300)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/photo/%s' % self.slug

    class Meta:
        ordering = ['name']
        verbose_name = _(u'Альбом')
        verbose_name_plural = _(u'Альбомы')


class Portfolio(models.Model):
    name = models.CharField(_(u'Название'), max_length=150)
    photo = ThumbnailerImageField(verbose_name=_(u'Фото'), upload_to='portfolios/', blank=True, null=True)
    youtube = models.URLField(_(u'Ссылка на YT'), blank=True, null=True)
    text = models.TextField(_(u'Текст'), max_length=500, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = _(u'Портфолио')
        verbose_name_plural = _(u'Портфолио')
