# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import operator
from itertools import chain

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from rest_framework.filters import BaseFilterBackend
from rest_framework.serializers import ValidationError


class MaestroHaystackFilter(BaseFilterBackend):
    """
    A filter backend that compiles a haystack compatible
    filtering query.
    """

    @staticmethod
    def build_filter(view, filters=None):
        """
        Creates a single SQ filter from querystring parameters that
        correspond to the SearchIndex fields that have been "registered"
        in `view.fields`.

        Default behavior is to `OR` terms for the same parameters, and `AND`
        between parameters.

        Any querystring parameters that are not registered in
        `view.fields` will be ignored.
        """

        terms = []
        exclude_terms = []
        search_models = ['expert', 'training', 'teaching', 'solution', 'rising', 'event', 'post']
        models = []

        if filters is None:
            filters = {}  # pragma: no cover
        filters.pop('page', None)
        for param, value in filters.items():
            # Skip if the parameter is not listed in the serializer's `fields`
            # or if it's in the `exclude` list.
            excluding_term = False
            param_parts = param.split("__")
            base_param = param_parts[0]  # only test against field without lookup
            negation_keyword = getattr(settings, "DRF_HAYSTACK_NEGATION_KEYWORD", "not")
            if len(param_parts) > 1 and param_parts[1] == negation_keyword:
                excluding_term = True
                param = param.replace("__%s" % negation_keyword, "")  # haystack wouldn't understand our negation
            if param == 'models':
                for model in value.split(","):
                    if model not in search_models:
                        raise ValidationError(_(u'Неизвестная модель'))
                    models.append(ContentType.objects.get(model=model).model_class())
                continue
            if view.serializer_class:
                try:
                    if hasattr(view.serializer_class.Meta, "field_aliases"):
                        old_base = base_param
                        base_param = view.serializer_class.Meta.field_aliases.get(base_param, base_param)
                        param = param.replace(old_base, base_param)  # need to replace the alias

                    fields = getattr(view.serializer_class.Meta, "fields", [])
                    exclude = getattr(view.serializer_class.Meta, "exclude", [])
                    search_fields = getattr(view.serializer_class.Meta, "search_fields", [])

                    if ((fields or search_fields) and base_param not in chain(fields,
                                                                              search_fields)) or base_param in exclude or not value:
                        continue

                except AttributeError:
                    raise ImproperlyConfigured("%s must implement a Meta class." %
                                               view.serializer_class.__class__.__name__)

            tokens = [token.strip() for token in value.split(view.lookup_sep)]
            field_queries = []

            for token in tokens:
                if token:
                    field_queries.append(view.query_object((param, token)))

            term = six.moves.reduce(operator.or_, filter(lambda x: x, field_queries))
            if excluding_term:
                exclude_terms.append(term)
            else:
                terms.append(term)

        terms = six.moves.reduce(operator.and_, filter(lambda x: x, terms)) if terms else []
        exclude_terms = six.moves.reduce(operator.and_, filter(lambda x: x, exclude_terms)) if exclude_terms else []
        return (terms, exclude_terms, models)

    def filter_queryset(self, request, queryset, view):
        applicable_filters, applicable_exclusions, models = self.build_filter(view,
                                                                              filters=self.get_request_filters(request))
        if models:
            queryset = queryset.models(*models)
        if applicable_filters:
            queryset = queryset.filter(applicable_filters)
        if applicable_exclusions:
            queryset = queryset.exclude(applicable_exclusions)
        return queryset

    def get_request_filters(self, request):
        return request.GET.copy()
