# -*- coding: utf-8 -*-
from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'maestro.ajax_views.home', name='home'),
    url(r'^company$', 'maestro.ajax_views.company', name='company'),
    url(r'^feedback$', 'maestro.ajax_views.feedback', name='feedback'),
    url(r'^news$', 'blog.views.news_list', name='news'),
    url(r'^news/(?P<slug>.*)$', 'blog.views.news_retrieve', name='news-detail'),
    url(r'^stats$', 'blog.views.posts_list', name='stats'),
    url(r'^stats/(?P<slug>.*)$', 'blog.views.posts_retrieve', name='stats-detail'),
    url(r'^trainers$', 'experts.views.experts_list', name='trainers'),
    url(r'^trainers/(?P<slug>.*)$', 'experts.views.experts_retrieve', name='trainers-detail'),
    url(r'^photo$', 'maestro.ajax_views.photo', name='photo'),
    url(r'^trainings$', 'courses.views.trainings_list', name='trainings'),
    url(r'^trainings/(?P<train_id>[0-9]+)$', 'courses.views.trainings_retrieve', name='trainings-retrieve'),
    url(r'^competences$', 'courses.views.competences_list', name='competences'),
    url(r'^competences/(?P<comp_id>[0-9]+)/teachings$', 'courses.views.teachings_list', name='teachings'),
    url(r'^competences/(?P<comp_id>[0-9]+)/teachings/(?P<teach_id>[0-9]+)$', 'courses.views.teachings_retrieve',
        name='teachings-retrieve'),
    url(r'^solutions$', 'courses.views.solutions_list', name='solutions'),
    url(r'^solutions/(?P<sol_id>[0-9]+)$', 'courses.views.solutions_retrieve', name='solutions-retrieve'),
    url(r'^risings$', 'courses.views.solutions_list', name='risings'),
    url(r'^risings/(?P<rise_id>[0-9]+)$', 'courses.views.risings_retrieve', name='risings-retrieve'),
    url(r'^events$', 'courses.views.events_list', name='events'),
    url(r'^events/(?P<ev_id>[0-9]+)$', 'courses.views.events_retrieve', name='events-retrieve'),
    url(r'^training-calendar$', 'maestro.ajax_views.trainings_calendar_list', name='calendar'),
    url(r'^training-calendar/(?P<slug>.*)$', 'maestro.ajax_views.trainings_calendar_retrieve',
        name='training-calendar-retrieve'),
    # url(r'^arhive/(?P<year>\d{4})', 'maestro.ajax_views.home', 'arhive'),
    # url(r'^arhive/(?P<year>\d{4})/(?P<slug>.*)', 'maestro.ajax_views.home', 'arhive-detail')
]
