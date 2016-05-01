# -*- coding: utf-8 -*-
from drf_haystack.serializers import HaystackSerializer
from experts.serializers import ExpertReadSerializer
from haystack import indexes
from rest_framework.serializers import CharField

from models import Training, Teaching, Solution, Rising, Event


class TrainingIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr="name")

    def get_model(self):
        return Training


class TeachingIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr="name")

    def get_model(self):
        return Teaching


class SolutionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr="name")

    def get_model(self):
        return Solution


class RisingIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr="name")

    def get_model(self):
        return Rising


class EventIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr="name")

    def get_model(self):
        return Event


class CourseSearchSerializer(HaystackSerializer):
    type = CharField(source='verbose_name')
    owner = ExpertReadSerializer(source='object.owner', read_only=True)
    url = CharField(source='object.get_absolute_url')


class TrainingSearchSerializer(CourseSearchSerializer):
    class Meta:
        index_classes = [TrainingIndex, ]
        fields = ["name", ]


class TeachingSearchSerializer(CourseSearchSerializer):
    class Meta:
        index_classes = [TeachingIndex, ]
        fields = ["name", ]


class SolutionSearchSerializer(CourseSearchSerializer):
    class Meta:
        index_classes = [SolutionIndex, ]
        fields = ["name", ]


class RisingSearchSerializer(CourseSearchSerializer):
    class Meta:
        index_classes = [RisingIndex, ]
        fields = ["name", ]


class EventSearchSerializer(CourseSearchSerializer):
    class Meta:
        index_classes = [EventIndex, ]
        fields = ["name", ]
