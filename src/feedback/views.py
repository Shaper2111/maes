# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.routers import SimpleRouter
from rest_framework.serializers import ValidationError
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import ModelViewSet

from models import Calendar, Call, Request
from serializers import CalendarSerializer, CallSerializer, RequestSerializer


class CalendarViewset(ModelViewSet):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

    def create(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            raise ValidationError(_(u'У вас уже есть файл календаря!'))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)


class CallViewset(ModelViewSet):
    queryset = Call.objects.all()
    serializer_class = CallSerializer
    permission_classes = [AllowAny, ]


class RequestViewset(ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [AllowAny, ]


router = SimpleRouter()
router.register(r'^calendar', CalendarViewset)
router.register(r'^calls', CallViewset)
router.register(r'^requests', RequestViewset)
