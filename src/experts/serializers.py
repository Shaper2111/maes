# -*- coding: utf-8 -*-
from django.utils import six
from maestro.utils import MaestroModelSerializer
from rest_framework.compat import OrderedDict
from rest_framework.serializers import PrimaryKeyRelatedField, ManyRelatedField

from models import Client, Expert


class ClientSerializer(MaestroModelSerializer):
    class Meta:
        model = Client


class ClientReadSerializer(MaestroModelSerializer):
    class Meta:
        model = Client
        fields = ('name', 'logo')


class ManyClientsField(ManyRelatedField):
    def to_representation(self, iterable):
        return [
            ClientReadSerializer(value).data
            for value in iterable
            ]


class ExpertSerializer(MaestroModelSerializer):
    clients = ManyClientsField(child_relation=PrimaryKeyRelatedField(queryset=Client.objects.all()), required=False)

    class Meta:
        model = Expert


class ExpertListSerializer(MaestroModelSerializer):
    class Meta:
        model = Expert
        fields = ('name', 'slug', 'avatar', 'intro')


class ExpertReadSerializer(MaestroModelSerializer):
    class Meta:
        model = Expert
        fields = ('id', 'name', 'avatar')


class PrimaryKeyExpertField(PrimaryKeyRelatedField):
    def use_pk_only_optimization(self):
        return False

    def to_representation(self, value):
        return ExpertReadSerializer(value).data

    @property
    def choices(self):
        return OrderedDict([
                               (
                                   six.text_type(item.pk),
                                   six.text_type(item)
                               )
                               for item in self.queryset.all()
                               ])
