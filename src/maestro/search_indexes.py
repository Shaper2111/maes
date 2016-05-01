# -*- coding: utf-8 -*-
from blog.search_indexes import PostIndex, PostSearchSerializer, NewsIndex, NewsSearchSerializer
from courses.search_indexes import TrainingIndex, TrainingSearchSerializer, TeachingIndex, TeachingSearchSerializer, \
    SolutionIndex, SolutionSearchSerializer, RisingIndex, RisingSearchSerializer, EventIndex, EventSearchSerializer
from drf_haystack.serializers import HaystackSerializer
from drf_haystack.viewsets import HaystackViewSet
from experts.search_indexes import ExpertIndex, ExpertSearchSerializer
from rest_framework import routers

from filters import MaestroHaystackFilter


class AggregateSerializer(HaystackSerializer):
    class Meta:
        serializers = {
            ExpertIndex: ExpertSearchSerializer,
            TrainingIndex: TrainingSearchSerializer,
            TeachingIndex: TeachingSearchSerializer,
            SolutionIndex: SolutionSearchSerializer,
            RisingIndex: RisingSearchSerializer,
            EventIndex: EventSearchSerializer,
            PostIndex: PostSearchSerializer,
            NewsIndex: NewsSearchSerializer
        }


class AggregateSearchViewSet(HaystackViewSet):
    serializer_class = AggregateSerializer
    filter_backends = [MaestroHaystackFilter]


router = routers.SimpleRouter()
router.register("search", AggregateSearchViewSet, base_name="search")
