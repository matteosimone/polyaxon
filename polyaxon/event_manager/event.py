from uuid import uuid1

from django.utils import timezone

from libs.date_utils import to_timestamp
from libs.json_utils import dumps_htmlsafe


class Attribute(object):
    def __init__(self, name, attr_type=str, is_datetime=False, is_uuid=False, is_required=True):
        self.name = name
        self.attr_type = attr_type
        self.is_datetime = is_datetime
        self.is_uuid = is_uuid
        self.is_required = is_required

    def extract(self, value):
        if value is None:
            return value
        if self.is_datetime:
            return to_timestamp(value)
        if self.is_uuid and not isinstance(value, str):
            return value.hex
        return self.attr_type(value)


class Event(object):
    __slots__ = ['uuid', 'data', 'datetime']

    event_type = None  # The event type should ideally follow subject.action
    attributes = ()
    actor_id = None

    def __init__(self, datetime=None, **items):
        self.uuid = uuid1()
        self.datetime = datetime or timezone.now()

        if self.event_type is None:
            raise ValueError('Event is missing a type')

        data = {}
        has_actor = False
        for attr in self.attributes:
            item_value = items.pop(attr.name, None)
            if attr.is_required and item_value is None:
                raise ValueError('{} is required (cannot be None)'.format(
                    attr.name,
                ))
            if self.actor_id and attr.name == self.actor_id:
                has_actor = True
            data[attr.name] = attr.extract(item_value)

        if self.actor_id and not has_actor:
            raise ValueError('Event {} requires an attribute specifying the actor id'.format(
                self.event_type
            ))

        if items:
            raise ValueError('Unknown attributes: {}'.format(
                ', '.join(items.keys()),
            ))

        self.data = data

    @classmethod
    def get_event_subject(cls):
        """Return the first part of the event_type

        e.g.

        >>> Event.event_type = 'experiment.deleted'
        >>> Event.get_event_subject() == 'experiment'
        """
        return cls.event_type.split('.')[0]

    @classmethod
    def get_event_action(cls):
        """Return the second part of the event_type

        e.g.

        >>> Event.event_type = 'experiment.deleted'
        >>> Event.get_event_action() == 'deleted'
        """
        if not cls.actor_id:
            return None
        return cls.event_type.split('.')[1]

    def serialize(self, dumps=True):
        data = {
            'uuid': self.uuid.hex,
            'timestamp': to_timestamp(self.datetime),
            'type': self.event_type,
            'data': self.data,
        }
        return dumps_htmlsafe(data) if dumps else data

    @classmethod
    def from_instance(cls, instance, **kwargs):
        values = {}
        for attr in cls.attributes:
            # TODO: add support for automatic dot props, e.g. 'user.id'
            values[attr.name] = kwargs.get(attr.name, getattr(instance, attr.name, None))
        return cls(**values)