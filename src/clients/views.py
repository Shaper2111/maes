# -*- coding: utf-8 -*-
from rest_framework.routers import SimpleRouter
from rest_framework.viewsets import ModelViewSet

from models import Client
from serializers import ClientSerializer


class ClientViewset(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


router = SimpleRouter()
router.register(r'^clients', ClientViewset)
