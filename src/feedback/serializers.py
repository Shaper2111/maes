# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from maestro.utils import MaestroModelSerializer
from rest_framework.serializers import RegexField

from models import Calendar, Call, Request


class CalendarSerializer(MaestroModelSerializer):
    class Meta:
        model = Calendar


class CallSerializer(MaestroModelSerializer):
    class Meta:
        model = Call


class RequestSerializer(MaestroModelSerializer):
    url = RegexField(r'^(\/|(\/competences\/[0-9]+\/))(training|teaching|rising|solution|event)s\/[0-9]+$',
                     required=True, write_only=True)

    def create(self, validated_data):
        type = validated_data.pop('url')
        ty = type.split("/")
        ct = ContentType.objects.get(model=ty[-2][0:-1])
        return Request.objects.create(content_type=ct, object_id=ty[-1], **validated_data)

    class Meta:
        model = Request
        exclude = ('content_type', 'object_id')
