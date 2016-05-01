# -*- coding: utf-8 -*-
from calendars.models import Calendar
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.routers import SimpleRouter
from rest_framework.viewsets import ModelViewSet

from models import Client, Expert
from serializers import ClientSerializer, ExpertListSerializer, ExpertSerializer


class ExpertResultsSetPagination(PageNumberPagination):
    page_size = 50


class ClientViewset(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ExpertViewset(ModelViewSet):
    queryset = Expert.objects.order_by('name')
    serializer_class = ExpertSerializer
    pagination_class = ExpertResultsSetPagination
    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ExpertListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ExpertListSerializer(queryset, many=True)
        return Response(serializer.data)


router = SimpleRouter()
router.register(r'^clients', ClientViewset)
router.register(r'^trainers', ExpertViewset)


def experts_list(request):
    experts = Expert.objects.order_by('name')[:50].values('name', 'slug', 'intro', 'avatar')
    return render_to_response('ajax_templates/experts/experts_list.html', {'trains': experts},
                              context_instance=RequestContext(request))


def experts_retrieve(request, slug):
    expert = get_object_or_404(Expert, slug=slug)
    trainings = Calendar.objects.future_courses()
    return render_to_response('ajax_templates/experts/experts_retrieve.html',
                              {'response': expert, 'trainings': trainings}, context_instance=RequestContext(request))
