# -*- coding: utf-8 -*-
from drf_haystack.serializers import HaystackSerializer
from experts.serializers import ExpertReadSerializer
from haystack import indexes
from rest_framework.serializers import CharField

from models import News, Post


class NewsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr="name")

    def get_model(self):
        return News


class NewsSearchSerializer(HaystackSerializer):
    type = CharField(source='verbose_name')
    owner = ExpertReadSerializer(source='object.owner', read_only=True)
    url = CharField(source='object.get_absolute_url')

    class Meta:
        index_classes = [NewsIndex, ]
        fields = ["name", ]


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr="name")

    def get_model(self):
        return Post


class PostSearchSerializer(HaystackSerializer):
    type = CharField(source='verbose_name')
    owner = ExpertReadSerializer(source='object.owner', read_only=True)
    url = CharField(source='object.get_absolute_url')

    class Meta:
        index_classes = [PostIndex, ]
        fields = ["name", ]
