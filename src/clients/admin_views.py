# -*- coding: utf-8 -*-
from rest_framework.routers import SimpleRouter
from rest_framework.viewsets import ModelViewSet

from admin_serializers import ClientAdminSerializer
from models import Client


class ClienAdminViewset(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientAdminSerializer


admin_router = SimpleRouter()
admin_router.register(r'^clients', ClienAdminViewset)
