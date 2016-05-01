# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import resolve


class HtmlSnapshotMiddleware(object):
    def process_request(self, request):
        escaped_fragment = request.GET.get('_escaped_fragment_', None)
        if not escaped_fragment:
            return None
        view, args, kwargs = resolve(escaped_fragment, urlconf=settings.AJAX_CRAWLING_URLCONF)
        if view:
            kwargs['request'] = request
            return view(*args, **kwargs)
        else:
            return None
