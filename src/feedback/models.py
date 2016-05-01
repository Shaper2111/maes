# -*- coding: utf-8 -*-
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from utils import send_email

DAY_TO_CALL = (
    ('TY', _(u'Сегодня')),
    ('TW', _(u'Завтра')),
    ('DA', _(u'Послезавтра')),
)


class Calendar(models.Model):
    file = models.FileField(_(u'Файл календаря'), upload_to='calendar/', blank=False)

    def __unicode__(self):
        return self.file

    class Meta:
        verbose_name = _(u'Календарь')
        verbose_name_plural = _(u'Календарь мероприятий')


class Call(models.Model):
    day = models.CharField(_(u'День звонка'), max_length=2, choices=DAY_TO_CALL, default='TY')
    time = models.TimeField(_(u'Время звонка'))
    phone = models.CharField(_(u'Телефон'), max_length=16, blank=True, null=True)

    def __unicode__(self):
        return self.id

    class Meta:
        verbose_name = _(u'Звонок')
        verbose_name_plural = _(u'Звонки')


post_save.connect(send_email, sender=Call)


class Request(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    name = models.CharField(_(u'ФИО'), max_length=80)
    phone = models.CharField(_(u'Телефон'), max_length=16, blank=True, null=True)
    email = models.EmailField(_(u'Адрес электронной почты'), max_length=50)
    comment = models.TextField(_(u'Комментарий'), max_length=350, blank=True)

    def __unicode__(self):
        return self.id

    class Meta:
        verbose_name = _(u'Заявка')
        verbose_name_plural = _(u'Заявки')


post_save.connect(send_email, sender=Request)
