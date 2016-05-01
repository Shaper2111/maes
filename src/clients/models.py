# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField


class Client(models.Model):
    name = models.CharField(_(u'Название'), max_length=50)
    logo = ThumbnailerImageField(verbose_name=_(u'Аватар'), upload_to='logos/', blank=True, null=True)

    class Meta:
        verbose_name = _(u'Клиент')
        verbose_name_plural = _(u'Клиенты')
