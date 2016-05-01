# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from views import router

urlpatterns = [
    url(r'', include(router.urls), name='clients'),
    url(r'^admin/', include(router.urls), name='admin_clients'),
]
