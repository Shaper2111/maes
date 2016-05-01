from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.views import serve as serve_static
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView

from .search_indexes import router
from .sitemaps import sitemaps

urlpatterns = [
    url(r'^api/', include('experts.urls')),
    url(r'^api/', include('courses.urls')),
    url(r'^api/', include('blog.urls')),
    url(r'^api/', include('feedback.urls')),
    url(r'^api/', include('calendars.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^api/login/$', 'rest_framework_jwt.views.obtain_jwt_token'),
]

if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^static/(?P<path>.*)$', never_cache(serve_static)),
                            (r'^images/(?P<path>.*)$', 'django.views.static.serve',
                             {'document_root': settings.MEDIA_ROOT})
                            )

urlpatterns += patterns('',
                        url(r'^robots\.txt$',
                            TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
                        url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
                            name='django.contrib.sitemaps.views.sitemap'),
                        url(r'^seo/', include('maestro.ajax_urls')),
                        url(r'^admin/.*$', 'maestro.views.admin_home', name='admin_home'),
                        url(r'^.*$', 'maestro.views.home', name='home'),
                        )
