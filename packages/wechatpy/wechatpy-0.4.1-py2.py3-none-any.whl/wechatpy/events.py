from __future__ import absolute_import, unicode_literals

from .fields import StringField, FloatField, IntegerField
from .messages import BaseMessage


EVENT_TYPES = {}


def register_event(event_type):
    def register(cls):
        EVENT_TYPES[event_type] = cls
        return cls
    return register


class BaseEvent(BaseMessage):
    type = 'event'
    event = ''


@register_event('subscribe')
class SubscribeEvent(BaseEvent):
    event = 'subscribe'


@register_event('unsubscribe')
class UnsubscribeEvent(BaseEvent):
    event = 'unsubscribe'


@register_event('subscribe_scan')
class SubscribeScanEvent(BaseEvent):
    event = 'subscribe_scan'
    scene_id = StringField('EventKey')
    ticket = StringField('Ticket')


@register_event('scan')
class ScanEvent(BaseEvent):
    event = 'scan'
    scene_id = StringField('EventKey')
    ticket = StringField('Ticket')


@register_event('location')
class LocationEvent(BaseEvent):
    event = 'location'
    latitude = FloatField('Latitude', 0.0)
    longitude = FloatField('Longitude', 0.0)
    precision = FloatField('Precision', 0.0)


@register_event('click')
class ClickEvent(BaseEvent):
    event = 'click'
    key = StringField('EventKey')


@register_event('view')
class ViewEvent(BaseEvent):
    event = 'view'
    url = StringField('EventKey')


@register_event('masssendjobfinish')
class MassSendJobFinishEvent(BaseEvent):
    event = 'masssendjobfinish'
    status = StringField('Status')
    total_count = IntegerField('TotalCount', 0)
    filter_count = IntegerField('FilterCount', 0)
    sent_count = IntegerField('SentCount', 0)
    error_count = IntegerField('ErrorCount', 0)


@register_event('templatesendjobfinish')
class TemplateSendJobFinishEvent(BaseEvent):
    event = 'templatesendjobfinish'
    status = StringField('Status')


@register_event('scancode_push')
class ScanCodePushEvent(BaseEvent):
    event = 'scancode_push'
    key = StringField('EventKey')
