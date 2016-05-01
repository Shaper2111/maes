# -*- coding: utf-8 -*-
from django.contrib.postgres.fields import DateRangeField
from django.db import models
from django.utils.encoding import force_text
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.fields import OrderedDict, ValidationError, api_settings, empty, DjangoValidationError, SkipField, \
    set_value
from rest_framework.metadata import SimpleMetadata
from rest_framework.utils.field_mapping import ClassLookupDict

from fields import Base64PDFField
from fields import TextField, DateRangeField as DateRangeSerializerField


class MaestroModelSerializer(serializers.ModelSerializer):
    serializers.ModelSerializer.serializer_field_mapping[models.TextField] = TextField
    serializers.ModelSerializer.serializer_field_mapping[DateRangeField] = DateRangeSerializerField
    serializers.ModelSerializer.serializer_field_mapping[models.ImageField] = Base64ImageField
    serializers.ModelSerializer.serializer_field_mapping[models.FileField] = Base64PDFField

    def to_internal_value(self, data):
        """
        Dict of native values <- Dict of primitive datatypes.
        """
        if not isinstance(data, dict):
            message = self.error_messages['invalid'].format(
                datatype=type(data).__name__
            )
            raise ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: [message]
            })

        ret = OrderedDict()
        errors = OrderedDict()
        fields = [
            field for field in self.fields.values()
            if (not field.read_only) or (field.default is not empty)
            ]

        for field in fields:
            validate_method = getattr(self, 'validate_' + field.field_name, None)
            primitive_value = field.get_value(data)
            try:
                validated_value = field.run_validation(primitive_value)
                if validate_method is not None:
                    validated_value = validate_method(validated_value)
            except ValidationError as exc:
                errors[unicode(field.label)] = exc.detail
            except DjangoValidationError as exc:
                errors[unicode(field.label)] = list(exc.messages)
            except SkipField:
                pass
            else:
                set_value(ret, field.source_attrs, validated_value)

        if errors:
            raise ValidationError(errors)

        return ret


class MaestroMetadata(SimpleMetadata):
    """
    This is the default metadata implementation.
    It returns an ad-hoc set of information about the view.
    There are not any formalized standards for `OPTIONS` responses
    for us to base this on.
    """
    label_lookup = ClassLookupDict({
        serializers.Field: 'field',
        serializers.PrimaryKeyRelatedField: 'select',
        serializers.BooleanField: 'boolean',
        serializers.NullBooleanField: 'boolean',
        TextField: 'textarea',
        DateRangeSerializerField: 'calendarPeriod',
        serializers.CharField: 'string',
        serializers.URLField: 'url',
        serializers.EmailField: 'email',
        serializers.RegexField: 'regex',
        serializers.SlugField: 'slug',
        serializers.IntegerField: 'integer',
        serializers.FloatField: 'float',
        serializers.DecimalField: 'decimal',
        serializers.DateField: 'date',
        serializers.DateTimeField: 'datetime',
        serializers.TimeField: 'time',
        serializers.ChoiceField: 'select',
        serializers.MultipleChoiceField: 'multiple choice',
        serializers.FileField: 'file upload',
        serializers.ImageField: 'image upload',
    })

    def get_serializer_info(self, serializer):
        """
        Given an instance of a serializer, return a dictionary of metadata
        about its fields.
        """
        if hasattr(serializer, 'child'):
            # If this is a `ListSerializer` then we want to examine the
            # underlying child serializer instance instead.
            serializer = serializer.child
        return self.iterate_fields(serializer.fields.items())

    def iterate_fields(self, fields):
        info = OrderedDict()
        for field_name, field in fields:
            if not field.read_only and field.__class__.__name__ != 'HiddenField':
                if not hasattr(field, 'fields'):
                    info[field_name] = self.get_field_info(field)
                else:
                    info[field_name] = self.iterate_fields(field.fields.items())
                    info[field_name].update({'type': field_name, 'read_only': False})
        return info

    def get_field_info(self, field):
        """
        Given an instance of a serializer field, return a dictionary
        of metadata about it.
        """
        field_info = OrderedDict()
        field_info['type'] = self.label_lookup[field]
        field_info['required'] = getattr(field, 'required', False)

        attrs = [
            'read_only', 'label', 'help_text',
            'min_length', 'max_length',
            'min_value', 'max_value'
        ]

        for attr in attrs:
            value = getattr(field, attr, None)
            if value is not None and value != '':
                field_info[attr] = force_text(value, strings_only=True)

        if not field_info.get('read_only') and hasattr(field, 'choices'):
            field_info['choices'] = [
                {
                    'value': choice_value,
                    'display_name': force_text(choice_name, strings_only=True)
                }
                for choice_value, choice_name in field.choices.items()
                ]

        return field_info


class ThumbnailSerializer(serializers.Serializer):
    small = serializers.SerializerMethodField()
    orig = serializers.SerializerMethodField()
    big = serializers.SerializerMethodField()

    def get_small(self, obj):
        try:
            return obj['small'].url
        except KeyError:
            return None

    def get_orig(self, obj):
        try:
            return obj.url
        except ValueError:
            return None

    def get_big(self, obj):
        try:
            return obj['big'].url
        except KeyError:
            return None
