# -*- coding: utf-8 -*-
from drf_haystack.serializers import HaystackSerializer
from haystack import indexes
from rest_framework.serializers import CharField

from models import Expert


class ExpertIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr="name")

    def get_model(self):
        return Expert


class ExpertSearchSerializer(HaystackSerializer):
    type = CharField(source='verbose_name')
    url = CharField(source='object.get_absolute_url')

    class Meta:
        index_classes = [ExpertIndex, ]
        fields = ["name", ]
