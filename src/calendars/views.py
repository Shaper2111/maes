# -*- coding: utf-8 -*-
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework_extensions.routers import ExtendedSimpleRouter

from models import Calendar, Archive, Portfolio
from serializers import CalendarSerializer, CalendarListSerializer, PortfolioSerializer


class ArchiveViewset(ReadOnlyModelViewSet):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer
    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        year = self.kwargs['year']
        if year:
            queryset = queryset.filter(archive__year=year)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = CalendarListSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = CalendarListSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response(Archive.objects.all().values_list('year', flat=True))


class CalendarViewset(ReadOnlyModelViewSet):
    queryset = Calendar.objects.future_courses()
    serializer_class = CalendarSerializer
    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CalendarListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CalendarListSerializer(queryset, many=True)
        return Response(serializer.data)


class PortfolioViewset(ModelViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer


router = ExtendedSimpleRouter()
router.register(r'^training-calendar', CalendarViewset, 'calendar')
router.register(r'^arhive(/(?P<year>\d{4}))?', ArchiveViewset, 'arhive')
router.register(r'^acts', PortfolioViewset, 'only-acts')
