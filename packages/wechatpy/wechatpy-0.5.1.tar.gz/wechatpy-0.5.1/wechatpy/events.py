from __future__ import absolute_import, unicode_literals

from .fields import StringField, FloatField, IntegerField, BaseField
from .messages import BaseMessage
from .utils import ObjectDict


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
    scan_code_info = BaseField('ScanCodeInfo', ObjectDict())

    @property
    def scan_type(self):
        return self.scan_code_info['ScanType']

    @property
    def scan_result(self):
        return self.scan_code_info['ScanResult']


@register_event('scancode_waitmsg')
class ScanCodeWaitMsgEvent(BaseEvent):
    event = 'scancode_waitmsg'
    key = StringField('EventKey')
    scan_code_info = BaseField('ScanCodeInfo', ObjectDict())

    @property
    def scan_type(self):
        return self.scan_code_info['ScanType']

    @property
    def scan_result(self):
        return self.scan_code_info['ScanResult']


@register_event('pic_sysphoto')
class PicSysPhotoEvent(BaseEvent):
    event = 'pic_sysphoto'
    key = StringField('EventKey')
    pictures_info = BaseField('SendPicsInfo', ObjectDict())

    @property
    def count(self):
        return self.pictures_info['Count']

    @property
    def pictures(self):
        return self.pictures_info['PicList']


@register_event('pic_photo_or_album')
class PicPhotoOrAlbumEvent(BaseEvent):
    event = 'pic_photo_or_album'
    key = StringField('EventKey')
    pictures_info = BaseField('SendPicsInfo', ObjectDict())

    @property
    def count(self):
        return self.pictures_info['Count']

    @property
    def pictures(self):
        return self.pictures_info['PicList']


@register_event('pic_weixin')
class PicWeChatEvent(BaseEvent):
    event = 'pic_weixin'
    key = StringField('EventKey')
    pictures_info = BaseField('SendPicsInfo', ObjectDict())

    @property
    def count(self):
        return self.pictures_info['Count']

    @property
    def pictures(self):
        return self.pictures_info['PicList']


@register_event('location_select')
class LocationSelectEvent(BaseEvent):
    event = 'location_select'
    key = StringField('EventKey')
    location_info = BaseField('SendLocationInfo', ObjectDict())

    @property
    def location_x(self):
        return self.location_info['Location_X']

    @property
    def location_y(self):
        return self.location_info['Location_Y']

    @property
    def location(self):
        return self.location_x, self.location_y

    @property
    def scale(self):
        return self.location_info['Scale']

    @property
    def label(self):
        return self.location_info['Label']

    @property
    def poiname(self):
        return self.location_info['Poiname']


@register_event('card_pass_check')
class CardPassCheckEvent(BaseEvent):
    event = 'card_pass_check'
    card_id = StringField('CardId')


@register_event('card_not_pass_check')
class CardNotPassCheckEvent(BaseEvent):
    event = 'card_not_pass_check'
    card_id = StringField('CardId')


@register_event('user_get_card')
class UserGetCardEvent(BaseEvent):
    event = 'user_get_card'
    card_id = StringField('CardId')
    is_given_by_friend = IntegerField('IsGiveByFriend')
    code = StringField('UserCardCode')


@register_event('user_del_card')
class UserDeleteCardEvent(BaseEvent):
    event = 'user_del_card'
    card_id = StringField('CardId')
    code = StringField('UserCardCode')
