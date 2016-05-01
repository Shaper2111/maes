# -*- coding: utf-8 -*-
from courses.fields import CourseRelatedField
from drf_extra_fields.fields import Base64ImageField
from experts.serializers import PrimaryKeyExpertField
from maestro.utils import MaestroModelSerializer
from maestro.utils import TextField
from rest_framework import serializers

from models import Calendar, Album, Portfolio


class CalendarSerializer(MaestroModelSerializer):
    course = CourseRelatedField(source='content_object', read_only=True)
    url = serializers.CharField(source='content_object.get_absolute_url')

    class Meta:
        model = Calendar
        exclude = ('id', 'content_type', 'object_id', 'year')


class CalendarListSerializer(MaestroModelSerializer):
    name = serializers.CharField(source='content_object.name')
    short = TextField(source='content_object.short')
    photo = Base64ImageField(source='content_object.photo')
    owner = PrimaryKeyExpertField(source='content_object.owner', read_only=True)

    class Meta:
        model = Calendar
        exclude = ('id', 'year', 'content_type', 'object_id')


class AlbumSerializer(MaestroModelSerializer):
    course = CourseRelatedField(source='content_object', read_only=True)
    url = serializers.CharField(source='content_object.get_absolute_url')

    class Meta:
        model = Album
        exclude = ('id', 'content_type', 'object_id')


class AlbumListSerializer(MaestroModelSerializer):
    class Meta:
        model = Album
        fields = ('name', 'slug')


class PortfolioSerializer(MaestroModelSerializer):
    class Meta:
        model = Portfolio
