# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField


class Client(models.Model):
    name = models.CharField(_(u'Название'), max_length=50)
    logo = ThumbnailerImageField(verbose_name=_(u'Аватар'), upload_to='logos/', blank=True, null=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/clients/%d' % self.id

    class Meta:
        ordering = ['-id']
        verbose_name = _(u'Клиент')
        verbose_name_plural = _(u'Клиенты')


class Expert(models.Model):
    name = models.CharField(_(u'Название'), max_length=150)
    slug = models.SlugField(_(u'Путь в адресной строке'), blank=False, unique=True)
    avatar = ThumbnailerImageField(verbose_name=_(u'Аватар'), upload_to='avatars/', blank=True, null=True)
    intro = models.TextField(_(u'Вступительный текст'), max_length=500, blank=True)
    full = models.TextField(_(u'Полный текст'), max_length=5000, blank=True)
    job = models.CharField(_(u'Должность'), max_length=150, blank=True, null=True)
    education = models.CharField(_(u'Образование'), max_length=150, blank=True, null=True)
    line = models.CharField(_(u'Специальность'), max_length=150, blank=True, null=True)
    skill = models.CharField(_(u'Квалификация'), max_length=150, blank=True, null=True)
    hits = models.IntegerField(_(u'Количество просмотров'), default=0)
    clients = models.ManyToManyField(Client, blank=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/trainers/%s' % self.slug

    class Meta:
        ordering = ['-id']
        verbose_name = _(u'Эксперт')
        verbose_name_plural = _(u'Эксперты')
