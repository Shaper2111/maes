# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from maestro.viewsets import NestedViewset
from rest_framework.response import Response
from rest_framework_extensions.routers import ExtendedSimpleRouter

from models import News, Post
from serializers import NewsSerializer, NewsListSerializer, PostSerializer, PostListSerializer


class NewsViewset(NestedViewset):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = NewsListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = NewsListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.add_view()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class PostViewset(NestedViewset):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PostListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = NewsListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.add_view()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


router = ExtendedSimpleRouter()
router.register(r'^news', NewsViewset, 'news')
router.register(r'^stats', PostViewset, 'posts')


def news_list(request):
    news = News.objects.all()[:10]
    return render_to_response('ajax_templates/blog/news_list.html', {'news': news},
                              context_instance=RequestContext(request))


def news_retrieve(request, slug):
    news = get_object_or_404(News, slug=slug)
    return render_to_response('ajax_templates/blog/news_retrieve.html', {'data': news},
                              context_instance=RequestContext(request))


def posts_list(request):
    posts = Post.objects.all()[:10]
    return render_to_response('ajax_templates/blog/posts_list.html', {'posts': posts},
                              context_instance=RequestContext(request))


def posts_retrieve(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render_to_response('ajax_templates/blog/posts_retrieve.html', {'data': post},
                              context_instance=RequestContext(request))
