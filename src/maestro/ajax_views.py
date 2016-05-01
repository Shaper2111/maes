# -*- coding: utf-8 -*-
from calendars.models import Calendar, Portfolio
from django.http import Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext


def home(request):
    trainings = Calendar.objects.future_courses()
    acts = Portfolio.objects.all()[:4]
    return render_to_response('ajax_templates/main.html', {'trainings': trainings, 'acts': acts},
                              context_instance=RequestContext(request))


def trainings_calendar_list(request):
    trainings = Calendar.objects.future_courses()
    return render_to_response('ajax_templates/courses/training-calendar_list.html', {'courses': trainings},
                              context_instance=RequestContext(request))


def trainings_calendar_retrieve(request, slug):
    calendars = Calendar.objects.future_courses()
    try:
        course = calendars.get(slug=slug).content_object
    except Calendar.DoesNotExist:
        raise Http404('No %s matches the given query.' % Calendar._meta.object_name)
    return render_to_response('ajax_templates/courses/courses_retrieve.html',
                              {'course': course, 'calendars': calendars}, context_instance=RequestContext(request))


def company(request):
    return render_to_response('ajax_templates/company.html', {}, context_instance=RequestContext(request))


def feedback(request):
    return render_to_response('ajax_templates/feedback.html', {}, context_instance=RequestContext(request))


def photo(request):
    videos = Portfolio.objects.all()[:10]
    return render_to_response('ajax_templates/portfolio.html', {'videos': videos},
                              context_instance=RequestContext(request))
