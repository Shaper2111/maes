# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from views import router

urlpatterns = [
    url(r'', include(router.urls), name='experts'),
]
