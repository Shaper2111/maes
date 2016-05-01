# -*- coding: utf-8 -*-
from maestro.utils import MaestroModelSerializer

from models import Client


class ClientSerializer(MaestroModelSerializer):
    class Meta:
        model = Client
