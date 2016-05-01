# -*- coding: utf-8 -*-
from calendars.models import Album, Calendar
from calendars.serializers import AlbumListSerializer
from django.db.models import Count
from django.shortcuts import get_object_or_404, get_list_or_404, render_to_response, RequestContext
from maestro.viewsets import NestedViewset, NestedGenericViewset
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.routers import ExtendedSimpleRouter

from models import Act, Competence, Training, Teaching, Solution, Rising, Event, Comment
from serializers import ActSerializer, PhotoSerializer, CompetenceSerializer, TrainingSerializer, \
    TrainingListSerializer, \
    TeachingSerializer, TeachingListSerializer, SolutionSerializer, SolutionListSerializer, RisingSerializer, \
    RisingListSerializer, EventSerializer, EventListSerializer, CommentSerializer


class AlonePhotoViewset(ModelViewSet):
    queryset = Act.objects.all()
    serializer_class = PhotoSerializer
    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        cat = self.kwargs['cat']
        if cat:
            queryset = queryset.filter(album__slug=cat)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = PhotoSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = PhotoSerializer(queryset, many=True)
        else:
            serializer = AlbumListSerializer(Album.objects.all(), many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        try:
            album = Album.objects.get(slug=self.kwargs['cat']).id
            serializer.save(**{'album_id': album})
        except Album.DoesNotExist:
            raise NotFound


class NestedActViewset(NestedGenericViewset):
    queryset = Act.objects.all()
    serializer_class = ActSerializer

    def filter_queryset_by_parents_lookups(self, queryset):
        return queryset.filter(album_id=self.get_parent_object())

    def get_parent_object(self):
        self.parents = self.get_parents_query_dict()
        try:
            return Album.objects.get(**self.parents).id
        except Album.DoesNotExist:
            raise NotFound

    def perform_create(self, serializer):
        serializer.save(**{'album_id': self.get_parent_object()})


class CompetenceViewset(NestedViewset):
    queryset = Competence.objects.all()
    serializer_class = CompetenceSerializer


class TrainingViewset(NestedViewset):
    queryset = Training.objects.all().annotate(null_dates=Count('calendars__dates'))
    serializer_class = TrainingSerializer
    filter_backends = (OrderingFilter,)
    ordering = ('-null_dates', '-calendars__dates',)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TrainingListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TrainingListSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        if instance.calendar:
            instance.calendar.delete()
        if instance.album:
            instance.album.delete()
        instance.delete()


class TeachingViewset(NestedViewset):
    queryset = Teaching.objects.all()
    serializer_class = TeachingSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TeachingListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TeachingListSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        if instance.calendar:
            instance.calendar.delete()
        if instance.album:
            instance.album.delete()
        instance.delete()


class SolutionViewset(NestedViewset):
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SolutionListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = SolutionListSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        if instance.calendar:
            instance.calendar.delete()
        instance.delete()


class RisingViewset(NestedViewset):
    queryset = Rising.objects.all().annotate(null_dates=Count('calendars__dates'))
    serializer_class = RisingSerializer
    filter_backends = (OrderingFilter,)
    ordering = ('-null_dates', '-calendars__dates',)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = RisingListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = RisingListSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        if instance.calendar:
            instance.calendar.delete()
        instance.delete()


class EventViewset(NestedViewset):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = EventListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = EventListSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        if instance.calendar:
            instance.calendar.delete()
        if instance.album:
            instance.album.delete()
        instance.delete()


class CommentViewset(NestedGenericViewset):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


router = ExtendedSimpleRouter()
router.register(r'^photo(/(?P<cat>[^/]*))?', AlonePhotoViewset, 'alone-acts-photos')
teachings = router.register(r'^competences', CompetenceViewset, 'competences').register(r'teachings', TeachingViewset,
                                                                                        'teachings',
                                                                                        parents_query_lookups=[
                                                                                            'competence_id'])
teachings.register(r'acts', NestedActViewset, 'teachings-acts', parents_query_lookups=['competence_id', 'object_id', ])
teachings.register(r'comments', CommentViewset, 'teachings-comments',
                   parents_query_lookups=['competence_id', 'object_id', ])
trainings = router.register(r'^trainings', TrainingViewset, 'trainings')
trainings.register(r'acts', NestedActViewset, 'trainings-acts', parents_query_lookups=['object_id', ])
trainings.register(r'comments', CommentViewset, 'trainings-comments', parents_query_lookups=['object_id', ])
router.register(r'^solutions', SolutionViewset, 'solutions').register(r'comments', CommentViewset, 'solutions-comments',
                                                                      parents_query_lookups=['object_id', ])
router.register(r'^risings', RisingViewset, 'risings').register(r'comments', CommentViewset, 'solutions-comments',
                                                                parents_query_lookups=['object_id', ])
events = router.register(r'^events', EventViewset, 'events')
events.register(r'acts', NestedActViewset, 'events-acts', parents_query_lookups=['object_id', ])
events.register(r'comments', CommentViewset, 'solutions-comments', parents_query_lookups=['object_id', ])


def trainings_list(request):
    courses = Training.objects.annotate(null_dates=Count('calendars__dates')).order_by('-null_dates',
                                                                                       '-calendars__dates', )[:10]
    calendars = Calendar.objects.future_courses()
    return render_to_response('ajax_templates/courses/trainings_list.html',
                              {'courses': courses, 'calendars': calendars}, context_instance=RequestContext(request))


def competences_list(request):
    courses = Competence.objects.all()[:10]
    calendars = Calendar.objects.future_courses()
    return render_to_response('ajax_templates/courses/competences_list.html',
                              {'courses': courses, 'calendars': calendars}, context_instance=RequestContext(request))


def teachings_list(request, comp_id):
    courses = get_list_or_404(Teaching, competence=comp_id)[:10]
    calendars = Calendar.objects.future_courses()
    return render_to_response('ajax_templates/courses/teachings_list.html',
                              {'courses': courses, 'calendars': calendars}, context_instance=RequestContext(request))


def solutions_list(request):
    courses = Solution.objects.all()[:10]
    calendars = Calendar.objects.future_courses()
    return render_to_response('ajax_templates/courses/solutions_list.html',
                              {'courses': courses, 'calendars': calendars}, context_instance=RequestContext(request))


def risings_list(request):
    courses = Rising.objects.all()[:10]
    calendars = Calendar.objects.future_courses()
    return render_to_response('ajax_templates/courses/risings_list.html', {'courses': courses, 'calendars': calendars},
                              context_instance=RequestContext(request))


def events_list(request):
    courses = Event.objects.all()[:10]
    calendars = Calendar.objects.future_courses()
    return render_to_response('ajax_templates/courses/events_list.html', {'courses': courses, 'calendars': calendars},
                              context_instance=RequestContext(request))


def trainings_retrieve(request, train_id):
    training = get_object_or_404(Training, id=train_id)
    calendars = Calendar.objects.future_courses()
    return render_to_response('ajax_templates/courses/courses_retrieve.html',
                              {'course': training, 'calendars': calendars}, context_instance=RequestContext(request))


def teachings_retrieve(request, comp_id, teach_id):
    teaching = get_object_or_404(Teaching, competence=comp_id, id=teach_id)
    calendars = Calendar.objects.future_courses()
    return render_to_response('ajax_templates/courses/courses_retrieve.html',
                              {'course': teaching, 'calendars': calendars}, context_instance=RequestContext(request))


def solutions_retrieve(request, sol_id):
    solution = get_object_or_404(Solution, id=sol_id)
    calendars = Calendar.objects.future_courses()
    return render_to_response('ajax_templates/courses/courses_retrieve.html',
                              {'course': solution, 'calendars': calendars}, context_instance=RequestContext(request))


def risings_retrieve(request, rise_id):
    rising = get_object_or_404(Rising, id=rise_id)
    calendars = Calendar.objects.future_courses()
    return render_to_response('ajax_templates/courses/courses_retrieve.html',
                              {'course': rising, 'calendars': calendars}, context_instance=RequestContext(request))


def events_retrieve(request, ev_id):
    event = get_object_or_404(Event, id=ev_id)
    calendars = Calendar.objects.future_courses()
    return render_to_response('ajax_templates/courses/courses_retrieve.html', {'course': event, 'calendars': calendars},
                              context_instance=RequestContext(request))
