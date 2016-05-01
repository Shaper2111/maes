# -*- coding: utf-8 -*-
from maestro.utils import MaestroModelSerializer

from models import News, Post


class NewsSerializer(MaestroModelSerializer):
    class Meta:
        model = News
        exclude = ('id',)


class NewsListSerializer(MaestroModelSerializer):
    class Meta:
        model = News
        fields = ('name', 'slug', 'short')


class PostSerializer(MaestroModelSerializer):
    class Meta:
        model = Post
        exclude = ('id',)


class PostListSerializer(MaestroModelSerializer):
    class Meta:
        model = Post
        fields = ('name', 'slug', 'short')
