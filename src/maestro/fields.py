# -*- coding: utf-8 -*-
import base64
import datetime
import imghdr
import uuid

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.utils.dateparse import parse_date
from django.utils.translation import ugettext_lazy as _
from psycopg2._range import DateRange
from rest_framework import ISO_8601
from rest_framework.serializers import CharField, Field
from rest_framework.serializers import FileField
from rest_framework.settings import api_settings
from rest_framework.utils import humanize_datetime


class TextField(CharField):
    pass


class DateRangeField(Field):
    initial = [None, None]
    format = api_settings.DATE_FORMAT
    input_formats = api_settings.DATE_INPUT_FORMATS
    default_error_messages = {
        'not_a_dict': _('Expected a dict of items but got type "{input_type}".'),
        'missing_attrs': _(u'Отсутствует lower или отсутсвует upper.'),
        'invalid': _('Date has wrong format. Use one of these formats instead: {format}.'),
        'datetime': _('Expected a date but got a datetime.'),
        'greater_than_lower': _(u'Значение lower не может быть меньше или равно upper.'),
    }

    def to_representation(self, obj):
        d = {'lower': obj.lower, 'upper': obj.upper}
        if self.format is not None:
            for k, v in d.iteritems():
                if not v:
                    continue
                # Applying a `DateField` to a datetime value is almost always
                # not a sensible thing to do, as it means naively dropping
                # any explicit or implicit timezone info.
                assert not isinstance(v, datetime.datetime), (
                    'Expected a `date`, but got a `datetime`. Refusing to coerce, '
                    'as this may mean losing timezone information. Use a custom '
                    'read-only field and deal with timezone issues explicitly.'
                )

                if self.format.lower() == ISO_8601:
                    if (isinstance(v, str)):
                        v = datetime.datetime.strptime(v, '%Y-%m-%d').date()
                    d[k] = v.isoformat()
                    continue
                d[k] = v.strftime(self.format)
        return d

    def to_internal_value(self, data):
        if not isinstance(data, dict) or not hasattr(data, '__len__') or len(data) != 2:
            self.fail('not_a_dict', input_type=type(data).__name__)
        if not data.has_key('lower') or not data.has_key('upper'):
            self.fail('missing_attrs')
        for k, v in data.iteritems():
            if not v:
                data[k] = None
                continue
            elif isinstance(v, datetime.date):
                continue
            elif isinstance(v, datetime.datetime):
                self.fail('datetime')
            try:
                data[k] = parse_date(v)
            except (ValueError, TypeError):
                humanized_format = humanize_datetime.date_formats(self.input_formats)
                self.fail('invalid', format=humanized_format)
        try:
            if data['lower'] >= data['upper'] and data['lower'] != None:
                self.fail('greater_than_lower', input_type=type(data).__name__)
        except TypeError:
            pass
        return DateRange(**data)


class Base64PDFField(FileField):
    """
    A django-rest-framework field for handling image-uploads through raw post data.
    It uses base64 for en-/decoding the contents of the file.
    """

    def to_internal_value(self, base64_data):
        # Check if this is a base64 string
        if base64_data in (None, '', [], (), {}):
            return None

        if isinstance(base64_data, basestring):
            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(base64_data)
            except TypeError:
                raise ValidationError(_("Please upload a valid image."))
            # Generate file name:
            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = imghdr.what(file_name, decoded_file)
            if file_extension != "pdf":
                raise ValidationError(_("The type of the file couldn't been determined."))
            complete_file_name = file_name + "." + file_extension
            data = ContentFile(decoded_file, name=complete_file_name)
            return super(Base64PDFField, self).to_internal_value(data)
        raise ValidationError(_('This is not an base64 string'))

    def to_representation(self, value):
        # Return url including domain name.
        return value.name
