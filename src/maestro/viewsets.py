# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import NotFound
from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework_extensions.settings import extensions_api_settings


class NestedViewset(NestedViewSetMixin, ModelViewSet):
    def get_parents_query_dict(self):
        result = {}
        if self.kwargs:
            kwarg_name = self.kwargs.keys()[0]
            if kwarg_name.startswith(extensions_api_settings.DEFAULT_PARENT_LOOKUP_KWARG_NAME_PREFIX):
                query_lookup = kwarg_name.replace(
                    extensions_api_settings.DEFAULT_PARENT_LOOKUP_KWARG_NAME_PREFIX,
                    '',
                    1
                )
                query_value = self.kwargs.get(kwarg_name)
                result[query_lookup] = query_value
        return result

    def perform_create(self, serializer):
        parents = self.get_parents_query_dict()
        serializer.save(**parents)


class NestedGenericViewset(NestedViewset):
    parents = None

    def get_queryset(self):
        if not self.get_parent_object():
            raise NotFound
        return self.filter_queryset_by_parents_lookups(
            super(NestedViewSetMixin, self).get_queryset()
        )

    def get_parent_object(self):
        self.parents = self.get_parents_query_dict()
        model = ContentType.objects.get_for_id(self.parents['content_type_id']).model_class()
        return model.objects.filter(id=self.parents['object_id']).exists()

    def get_parents_query_contenttype(self):
        # TODO: Есть способ получше??
        child_model = self.serializer_class.Meta.model.__name__
        path = self.request.path.split('/')
        for p in path:
            if child_model.lower() + 's' in p:
                model_name = path[path.index(p) - 2]
        ct = ContentType.objects.get(model=model_name[:-1]).id
        return ct

    def get_parents_query_dict(self):
        result = {}
        for kwarg_name in self.kwargs:
            if kwarg_name.startswith(
                    extensions_api_settings.DEFAULT_PARENT_LOOKUP_KWARG_NAME_PREFIX) and not kwarg_name.endswith(
                'competence_id'):
                query_lookup = kwarg_name.replace(
                    extensions_api_settings.DEFAULT_PARENT_LOOKUP_KWARG_NAME_PREFIX,
                    '',
                    1
                )
                query_value = self.kwargs.get(kwarg_name)
                result[query_lookup] = query_value
        result['content_type_id'] = self.get_parents_query_contenttype()
        return result
