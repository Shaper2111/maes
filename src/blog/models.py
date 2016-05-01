# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField


class News(models.Model):
    name = models.CharField(_(u'Название'), max_length=300)
    slug = models.SlugField(_(u'Путь в адресной строке'), blank=False, unique=True, max_length=300)
    photo = ThumbnailerImageField(_(u'Фото'), upload_to='news', blank=True, null=True)
    short = models.TextField(_(u'Вступительный текст'), max_length=500)
    body = models.TextField(_(u'Текст записи'), max_length=5000)
    metakey = models.CharField(_(u'Ключевые слова'), max_length=300, null=True)
    metadesc = models.TextField(_(u'Ключевое описание'), max_length=1000, null=True)
    views = models.IntegerField(_(u'Просмотры'), default=0, blank=False)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/news/%s' % self.slug

    def add_view(self):
        self.views = models.F('views') + 1
        self.save(update_fields=['views'])
        self.refresh_from_db(fields=['views'])

    class Meta:
        ordering = ["-id"]
        verbose_name = _(u'Новость')
        verbose_name_plural = _(u'Новости')


class Post(models.Model):
    name = models.CharField(_(u'Название'), max_length=300)
    slug = models.SlugField(_(u'Путь в адресной строке'), blank=False, unique=True, max_length=300)
    photo = ThumbnailerImageField(_(u'Фото'), upload_to='posts', blank=True, null=True)
    short = models.TextField(_(u'Вступительный текст'), max_length=500)
    body = models.TextField(_(u'Текст записи'), max_length=5000)
    metakey = models.CharField(_(u'Ключевые слова'), max_length=300, null=True)
    metadesc = models.TextField(_(u'Ключевое описание'), max_length=1000, null=True)
    views = models.IntegerField(_(u'Просмотры'), default=0, blank=False)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/stats/%s' % self.slug

    def add_view(self):
        self.views = models.F('views') + 1
        self.save(update_fields=['views'])
        self.refresh_from_db(fields=['views'])

    class Meta:
        ordering = ["-id"]
        verbose_name = _(u'Статья')
        verbose_name_plural = _(u'Статьи')
