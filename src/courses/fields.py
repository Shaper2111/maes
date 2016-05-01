# -*- coding: utf-8 -*-
from rest_framework.serializers import RelatedField

from models import Training, Teaching, Rising, Solution, Event
from serializers import TrainingSerializer, TeachingSerializer, RisingSerializer, SolutionSerializer, EventSerializer


class CourseRelatedField(RelatedField):
    """
    A custom field to use for the `tagged_object` generic relationship.
    """

    def to_representation(self, value):
        """
        Serialize tagged objects to a simple textual representation.
        """
        if isinstance(value, Training):
            serializer = TrainingSerializer(value)
        elif isinstance(value, Teaching):
            serializer = TeachingSerializer(value)
        elif isinstance(value, Rising):
            serializer = RisingSerializer(value)
        elif isinstance(value, Solution):
            serializer = SolutionSerializer(value)
        elif isinstance(value, Event):
            serializer = EventSerializer(value)
        else:
            raise Exception('Unexpected type of tagged object')

        return serializer.data
