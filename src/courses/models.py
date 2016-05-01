# -*- coding: utf-8 -*-
from calendars.models import Calendar, Album
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from experts.models import Expert


class CalendarMixin(object):
    @property
    def calendar(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        try:
            return Calendar.objects.get(content_type=content_type, object_id=self.id)
        except Calendar.DoesNotExist:
            return None


class AlbumMixin(object):
    @property
    def album(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        try:
            return Album.objects.get(content_type=content_type, object_id=self.id)
        except Album.DoesNotExist:
            return None


class Act(models.Model):
    name = models.CharField(_(u'Название'), max_length=150)
    photo = ThumbnailerImageField(verbose_name=_(u'Фото'), upload_to='act_photos/', blank=True, null=True)
    youtube = models.URLField(_(u'Ссылка на YT'), blank=True, null=True)
    text = models.TextField(_(u'Текст'), max_length=500, blank=True, null=True)
    slug = models.SlugField(_(u'Путь в адресной строке'), unique=True, max_length=150)
    album = models.ForeignKey(Album, verbose_name=_(u'Альбом'), null=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '%s/%s/' % (self.album.get_absolute_url(), self.slug)

    class Meta:
        ordering = ['-id']
        verbose_name = _(u'Портфолио')
        verbose_name_plural = _(u'Портфолио')


class Competence(models.Model):
    name = models.CharField(_(u'Название'), max_length=150)
    photo = ThumbnailerImageField(verbose_name=_(u'Фото'), upload_to='competence_photos/', blank=True, null=True)
    text = models.TextField(_(u'Описание'), max_length=500, blank=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/competences/%i' % self.id

    class Meta:
        ordering = ['-id']
        verbose_name = _(u'Компетенция')
        verbose_name_plural = _(u'Компетенции')


class Course(CalendarMixin, models.Model):
    name = models.CharField(_(u'Название'), max_length=300)
    short = models.TextField(_(u'Вступительный текст'), max_length=500, null=True)
    text = models.TextField(_(u'Описание'), max_length=5000, blank=True)
    owner = models.ForeignKey(Expert, verbose_name=_(u'Ведущий'), blank=True, null=True)
    price = models.PositiveIntegerField(_(u'Стоимость'), default=0)
    metakey = models.CharField(_(u'Ключевые слова'), max_length=300, null=True)
    metadesc = models.TextField(_(u'Ключевое описание'), max_length=1000, null=True)
    views = models.IntegerField(_(u'Просмотры'), default=0, blank=False)
    calendars = GenericRelation(Calendar)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/%s/%i' % (self._meta.model_name + 's', self.id)

    class Meta:
        ordering = ['-id']
        abstract = True


class Training(AlbumMixin, Course):
    photo = ThumbnailerImageField(verbose_name=_(u'Фото'), upload_to='training_photos/', blank=True, null=True)
    program = models.FileField(verbose_name=_(u'Программа'), upload_to='training_programs/', blank=True, null=True)

    class Meta:
        ordering = ['-id']
        verbose_name = _(u'Тренинг')
        verbose_name_plural = _(u'Тренинги для руководителей')


class Teaching(AlbumMixin, Course):
    photo = ThumbnailerImageField(verbose_name=_(u'Фото'), upload_to='teaching_photos/', blank=True, null=True)
    program = models.FileField(verbose_name=_(u'Программа'), upload_to='teaching_programs/', blank=True, null=True)
    competence = models.ForeignKey(Competence, verbose_name=_(u'Компетенция'), related_name='teachings', blank=False)

    def get_absolute_url(self):
        return '/competences/%i/teachings/%i' % (self.competence_id, self.id)

    class Meta:
        ordering = ['-id']
        verbose_name = _(u'Обучение')
        verbose_name_plural = _(u'Обучение сотрудников')


class Solution(Course):
    photo = ThumbnailerImageField(verbose_name=_(u'Фото'), upload_to='solution_photos/', blank=True, null=True)
    program = models.FileField(verbose_name=_(u'Программа'), upload_to='solution_programs/', blank=True, null=True)

    class Meta:
        ordering = ['-id']
        verbose_name = _(u'Решение')
        verbose_name_plural = _(u'Решения для бизнеса')


class Rising(Course):
    photo = ThumbnailerImageField(verbose_name=_(u'Фото'), upload_to='rising_photos/', blank=True, null=True)
    licence = models.FileField(verbose_name=_(u'Лицензия'), upload_to='rising_licences/', blank=True, null=True)

    class Meta:
        ordering = ['-id']
        verbose_name = _(u'Повышение')
        verbose_name_plural = _(u'Повышение квалификации')


class Event(AlbumMixin, Course):
    photo = ThumbnailerImageField(verbose_name=_(u'Фото'), upload_to='event_photos/', blank=True, null=True)

    class Meta:
        ordering = ['-id']
        verbose_name = _(u'Мероприятие')
        verbose_name_plural = _(u'Интеллектуальные игры')


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    name = models.CharField(_(u'ФИО'), max_length=150)
    photo = ThumbnailerImageField(verbose_name=_(u'Фото'), upload_to='comments/', blank=True, null=True)
    text = models.TextField(_(u'Текст'), max_length=500)

    def get_absolute_url(self):
        return '%scomments/%i/' % (self.content_object.get_absolute_url(), self.id)
