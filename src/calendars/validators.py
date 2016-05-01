# -*- coding: utf-8 -*-
from rest_framework.validators import UniqueValidator


class CalendarUniqueValidator(UniqueValidator):
    def set_context(self, serializer_field):
        """
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        # Determine the underlying model field name. This may not be the
        # same as the serializer field name if `source=<>` is set.
        self.field_name = serializer_field.source_attrs[0]
        # Determine the existing instance, if this is an update operation.
        self.instance = getattr(serializer_field.root.instance, 'calendar', None)


class AlbumUniqueValidator(UniqueValidator):
    def set_context(self, serializer_field):
        """
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        # Determine the underlying model field name. This may not be the
        # same as the serializer field name if `source=<>` is set.
        self.field_name = serializer_field.source_attrs[0]
        # Determine the existing instance, if this is an update operation.
        self.instance = getattr(serializer_field.root.instance, 'album', None)
