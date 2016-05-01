# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template.context import RequestContext


def home(request):
    return render_to_response('base.html', {}, context_instance=RequestContext(request))


def admin_home(request):
    return render_to_response('admin/base.html', {}, context_instance=RequestContext(request))
