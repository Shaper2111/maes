# -*- coding: utf-8 -*-
from calendars.models import Calendar, Album
from calendars.validators import CalendarUniqueValidator, AlbumUniqueValidator
from django.utils.translation import ugettext_lazy as _
from experts.serializers import Expert, PrimaryKeyExpertField
from maestro.utils import MaestroModelSerializer
from rest_framework.serializers import SlugField

from models import Act, Competence, Training, Teaching, Solution, Rising, Event, Comment


class OnlyCalendarSerializer(MaestroModelSerializer):
    slug = SlugField(label=_(u'Путь в адресной строке'), max_length=300,
                     validators=[CalendarUniqueValidator(queryset=Calendar.objects.all())])

    class Meta:
        model = Calendar
        fields = ('slug', 'dates', 'archive')


class OnlyAlbumSerializer(MaestroModelSerializer):
    slug = SlugField(label=_(u'Путь в адресной строке'), max_length=300,
                     validators=[AlbumUniqueValidator(queryset=Album.objects.all())])

    class Meta:
        model = Album
        fields = ('name', 'slug')


class PhotoSerializer(MaestroModelSerializer):
    class Meta:
        model = Act
        exclude = ('id', 'album')


class VideoSerializer(MaestroModelSerializer):
    class Meta:
        model = Act
        exclude = ('id', 'photo', 'album')


class ActSerializer(MaestroModelSerializer):
    class Meta:
        model = Act
        exclude = ('album',)


class CompetenceSerializer(MaestroModelSerializer):
    class Meta:
        model = Competence


class CourseSerializer(MaestroModelSerializer):
    owner = PrimaryKeyExpertField(label=_(u'Эксперт'), queryset=Expert.objects.all())
    calendar = OnlyCalendarSerializer()
    album = OnlyAlbumSerializer()

    def create(self, validated_data):
        calendar = validated_data.pop('calendar', None)
        album = validated_data.pop('album', None)
        model = self.Meta.model.objects.create(**validated_data)
        if calendar:
            Calendar.objects.create(content_object=model, **calendar)
        if album:
            Album.objects.create(content_object=model, **album)
        return model

    def update(self, instance, validated_data):
        calendar = validated_data.pop('calendar', None)
        album = validated_data.pop('album', None)
        if calendar:
            try:
                cal = instance.calendar
                for attr, value in calendar.items():
                    setattr(cal, attr, value)
                cal.save()
            except AttributeError:
                Calendar.objects.create(content_object=instance, **calendar)
        if album:
            try:
                al = instance.album
                for attr, value in album.items():
                    setattr(al, attr, value)
                al.save()
            except AttributeError:
                Album.objects.create(content_object=instance, **album)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class TrainingSerializer(CourseSerializer):
    class Meta:
        model = Training


class TrainingListSerializer(CourseSerializer):
    class Meta:
        model = Training
        exclude = ('text', 'metakey', 'metadesc', 'program')


class TeachingSerializer(CourseSerializer):
    class Meta:
        model = Teaching
        exclude = ('competence',)


class TeachingListSerializer(CourseSerializer):
    class Meta:
        model = Teaching
        exclude = ('text', 'competence', 'metakey', 'metadesc', 'program')


class SolutionSerializer(CourseSerializer):
    class Meta:
        model = Solution
        exclude = ('album',)


class SolutionListSerializer(CourseSerializer):
    class Meta:
        model = Solution
        exclude = ('album', 'text', 'metakey', 'metadesc', 'program')


class RisingSerializer(CourseSerializer):
    class Meta:
        model = Rising
        exclude = ('album',)


class RisingListSerializer(CourseSerializer):
    class Meta:
        model = Rising
        exclude = ('album', 'text', 'metakey', 'metadesc', 'licence')


class EventSerializer(CourseSerializer):
    class Meta:
        model = Event


class EventListSerializer(CourseSerializer):
    class Meta:
        model = Event
        exclude = ('text', 'metakey', 'metadesc')


class CommentSerializer(MaestroModelSerializer):
    class Meta:
        model = Comment
        exclude = ('content_type', 'object_id')
