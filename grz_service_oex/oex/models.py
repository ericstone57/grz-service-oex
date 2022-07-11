import re
import urllib
from datetime import datetime

import requests
from django.core.paginator import Paginator, EmptyPage
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import make_naive, make_aware
from django.utils.translation import ugettext_lazy as _
from ks_shared.django.model_utils import BaseModel, upload_to, BaseModelSoftDeletable
from model_utils import Choices, FieldTracker
from model_utils.fields import MonitorField, StatusField
from taggit.managers import TaggableManager
from taggit.models import TagBase, CommonGenericTaggedItemBase, GenericTaggedItemBase, TaggedItemBase, Tag

from grz_service_oex.user.models import User


class LinkType(BaseModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Link(BaseModel):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(LinkType, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    url = models.CharField(max_length=512, blank=True, default='')
    wxmp_appid = models.CharField(max_length=100, blank=True, default='')
    wxmp_pagepath = models.CharField(max_length=512, blank=True, default='')

    @property
    def type_code(self):
        return self.type.code

    def __str__(self):
        return self.name


class Banner(BaseModel):
    name = models.CharField(max_length=100)
    link = models.ForeignKey(Link, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    pic = models.ImageField(upload_to=upload_to)
    display_order = models.IntegerField(default=100)
    STATUS = Choices('draft', 'published')
    status = StatusField(choices_name='STATUS', default=STATUS.draft)
    published_at = MonitorField(monitor='status', when=['published'], blank=True, null=True, default=None)
    BELONG_TO_STATUS = Choices('user', 'storekeeper')
    belong_to = StatusField(choices_name='BELONG_TO_STATUS', default=BELONG_TO_STATUS.user)

    def __str__(self):
        return self.name

    @property
    def pic_link(self):
        if not self.pic:
            return ''
        if self.belong_to == 'user':
            return f'{self.pic.url}?x-oss-process=image/resize,m_fill,w_750,h_500'
        else:
            return f'{self.pic.url}?x-oss-process=image/resize,m_fill,w_750,h_350'

    @classmethod
    def retrieve_all(cls, belong_to: str = 'user'):
        return cls.objects.filter(
            status=cls.STATUS.published,
            belong_to=belong_to
        ).order_by('display_order', '-modified')


class TaggedThrough(GenericTaggedItemBase):
    object_id = models.CharField(max_length=50, verbose_name=_('Object id'), db_index=True)
    tag = models.ForeignKey(
        Tag, related_name="%(app_label)s_%(class)s_items", on_delete=models.CASCADE
    )
    is_strike_through = models.BooleanField(default=False)


class Space(BaseModel):
    title = models.CharField(max_length=255)
    # 670 x 380, in detail
    cover = models.ImageField(upload_to=upload_to, blank=True, null=True, default=None, help_text='670 x 380')
    # 190 x 190, in list
    cover_s = models.ImageField(upload_to=upload_to, blank=True, null=True, default=None, help_text='190 x 190')

    address = models.CharField(max_length=512, blank=True, default='')
    province = models.CharField(max_length=100, blank=True, default='')
    city = models.CharField(max_length=100, blank=True, default='')
    district = models.CharField(max_length=100, blank=True, default='')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, default=None)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, default=None)

    space_area = models.IntegerField(blank=True, default=0)
    contact_cellphone = models.CharField(max_length=20, blank=True, default='')

    intro = models.CharField(max_length=2000, blank=True, default='')
    opentime_from = models.TimeField(blank=True, null=True, default=None)
    opentime_to = models.TimeField(blank=True, null=True, default=None)

    tags = TaggableManager(through=TaggedThrough, blank=True)
    favorite_count = models.IntegerField(default=0)

    display_order = models.IntegerField(default=100)
    STATUS = Choices('draft', 'published')
    status = StatusField(choices_name='STATUS', default=STATUS.draft)
    published_at = MonitorField(monitor='status', when=['published'], blank=True, null=True, default=None)

    storekeeper = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.SET_NULL,
                                    related_name='storekeeper', related_query_name='storekeeper')
    VERIFY_STATUS = Choices('pending', 'rejected', 'accepted')
    verify_status = StatusField(choices_name='VERIFY_STATUS', default=VERIFY_STATUS.pending)
    accepted_at = MonitorField(monitor='verify_status', when=['accepted'], blank=True, null=True, default=None)
    accepted_by = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.SET_NULL,
                                    related_name='accepted_spaces')
    rejected_at = MonitorField(monitor='verify_status', when=['rejected'], blank=True, null=True, default=None)
    rejected_by = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.SET_NULL,
                                    related_name='rejected_spaces')
    rejected_reason = models.TextField(default=None, blank=True, null=True)

    # the tracker
    tracker = FieldTracker()

    def __str__(self):
        return self.title

    def convert_address_2_geolocation(self):
        if self.address:
            # gcj02 location
            # TODO: rewrite as service
            url = f'https://restapi.amap.com/v3/geocode/geo?key=6f1b7893a35936cac56dca3f5f2786a2&address={urllib.parse.quote_plus(self.address)}'
            resp = requests.get(url).json()
            if resp['status'] == '1':
                location = resp['geocodes'][0]['location'].split(',')
                self.province = resp['geocodes'][0]['province']
                self.city = resp['geocodes'][0]['city']
                self.longitude = location[0]
                self.latitude = location[1]
                self.save()

    @property
    def cover_link(self):
        return f'{self.cover.url}!670_380_resize_pad' if self.cover else ''

    @property
    def cover_s_link(self):
        return f'{self.cover_s.url}!190_190_cut' if self.cover_s else ''

    @property
    def tags_all(self):
        return [{
            'id': tagged.tag.id,
            'name': tagged.tag.name,
            'slug': tagged.tag.slug,
            'is_strike_through': tagged.is_strike_through
        } for tagged in TaggedThrough.objects.filter(object_id=self.id)]

    @property
    def work_spaces(self):
        return [{
            'id': space.id,
            'title': space.title,
            'cover': space.cover_link
        } for space in WorkSpace.objects.filter(space=self)]

    @property
    def space_pics(self):
        return self.retrieve_space_pics()

    def retrieve_space_pics(self):
        qs_outside = SpacePicture.objects.filter(space=self, category=SpacePicture.CATEGORY_STATUS.outside).order_by('created')
        qs_inside = SpacePicture.objects.filter(space=self, category=SpacePicture.CATEGORY_STATUS.inside).order_by('created')
        qs_other = SpacePicture.objects.filter(space=self, category=SpacePicture.CATEGORY_STATUS.other).order_by('created')
        pics = []
        for item in qs_outside:
            pics.append(item.src)
        for item in qs_inside:
            pics.append(item.src)
        for item in qs_other:
            pics.append(item.src)
        return pics

    @classmethod
    def retrieve_all(cls, user_id: str = None):
        qs = cls.objects.filter(status=cls.STATUS.published)
        if user_id:
            qs = qs.filter(storekeeper_id=user_id)
        qs = qs.order_by('display_order', '-modified')
        return qs

    @classmethod
    def retrieve_storekeeper_status(cls, user_id):
        q = cls.objects.filter(storekeeper_id=user_id)
        if q.filter(verify_status=cls.VERIFY_STATUS.accepted, status=cls.STATUS.published).count():
            return {'status': 'ok'}
        if q.filter(verify_status=cls.VERIFY_STATUS.rejected).count() == 1:
            msg_thread = MessageThread.objects.filter(receiver_id=user_id, type='sys', sender__openid='sys').first()
            return {'status': 'rejected', 'msg_thread': msg_thread.id}
        if q.filter(verify_status=cls.VERIFY_STATUS.pending).count() == 1:
            return {'status': 'pending'}
        return {'status': 'none'}

    @classmethod
    def retrieve_by_geolocation(cls, st_geo, user_geo, per_page=50, page_index=1):
        """
        st_geo, search through geolocation
        user_geo, user geolocation, used to calculate distance to destination
        use 116.481028,39.989643 format as parameter for geolocation
        """
        if not bool(re.match(r'^\d+.\d+,\d+.\d+', st_geo)):
            raise ValueError('st_geo, invalid search geolocation.')

        if user_geo and not bool(re.match(r'^\d+.\d+,\d+.\d+', user_geo)):
            raise ValueError('user_geo, invalid user geolocation.')

        search_geo = st_geo.split(',')
        user_geo = user_geo.split(',')

        select = "SELECT id, 0 as distance "
        if user_geo:
            select = "SELECT id, " \
                     "st_distancesphere(" \
                     " st_setsrid(st_makepoint(longitude, latitude), 4326), " \
                     " st_setsrid(st_makepoint(%s, %s), 4326)" \
                     ") as distance "

        criteria = "AND st_distancesphere(" \
                   " st_setsrid(st_makepoint(longitude, latitude), 4326)," \
                   " st_setsrid(st_makepoint(%s, %s), 4326)" \
                   ") <= %s "

        sql = select + " FROM oex_space WHERE status = 'published' " + criteria + " ORDER BY distance ASC"

        if user_geo:
            qs = cls.objects.raw(sql, [user_geo[0], user_geo[1], search_geo[0], search_geo[1], 50000])
        else:
            qs = cls.objects.raw(sql, [search_geo[0], search_geo[1], 50000])

        page = Paginator(qs, per_page)
        try:
            return page.page(page_index).object_list
        except EmptyPage:
            return []

    def accepted(self, by_user_id: str):
        self.verify_status = self.VERIFY_STATUS.accepted
        self.accepted_by_id = by_user_id
        self.status = self.STATUS.published

        if not self.cover:
            pic_obj = SpacePicture.objects.filter(space=self, category='outside').order_by('created').first()
            self.cover = pic_obj.file
            self.cover_s = pic_obj.file

        self.save()
        self.convert_address_2_geolocation()

    def rejected(self, by_user_id: str):
        self.verify_status = self.VERIFY_STATUS.rejected
        # TODO: reject by user, reject at, reject history?
        self.save()


@receiver(post_save, sender=Space)
def process_post_space_created(sender, instance: Space = None, created=False, **kwargs):
    if created:
        instance.convert_address_2_geolocation()


class SpacePicture(BaseModel):
    CATEGORY_STATUS = Choices('outside', 'inside', 'other')
    category = StatusField(choices_name='CATEGORY_STATUS', default=CATEGORY_STATUS.outside)
    pic = models.ImageField(upload_to=upload_to)
    space = models.ForeignKey(Space, on_delete=models.CASCADE)

    @property
    def src(self):
        return f'{self.pic.url}!670_380_resize_pad' if self.pic else ''


class WorkSpace(BaseModel):
    title = models.CharField(max_length=255)
    # 555 x 380
    cover = models.ImageField(upload_to=upload_to, help_text='555 x 380')

    space = models.ForeignKey(Space, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    @property
    def cover_link(self):
        return self.cover.url if self.cover else ''


class WorkSpacePosition(BaseModel):
    title = models.CharField(max_length=100)
    work_space = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Exhibition(BaseModel):
    title = models.CharField(max_length=255)
    # 670 x 380, in detail
    cover = models.ImageField(upload_to=upload_to)
    # 190 x 190, in list
    cover_s = models.ImageField(upload_to=upload_to)
    start_at = models.DateTimeField(blank=True, null=True, default=None)
    end_at = models.DateTimeField(blank=True, null=True, default=None)
    favorite_count = models.IntegerField(default=0)
    intro = models.CharField(max_length=2000, blank=True, default='')
    curator = models.CharField(max_length=512, blank=True, default='')
    author = models.CharField(max_length=512, blank=True, default='')

    space = models.ForeignKey(Space, on_delete=models.SET_NULL, blank=True, null=True, default=None)

    display_order = models.IntegerField(default=100)
    STATUS = Choices('draft', 'published')
    status = StatusField(choices_name='STATUS', default=STATUS.draft)
    published_at = MonitorField(monitor='status', when=['published'], blank=True, null=True, default=None)

    VERIFY_STATUS = Choices('pending', 'rejected', 'accepted')
    verify_status = StatusField(choices_name='VERIFY_STATUS', default=VERIFY_STATUS.pending)
    accepted_at = MonitorField(monitor='verify_status', when=['accepted'], blank=True, null=True, default=None)
    accepted_by = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.SET_NULL,
                                    related_name='accepted_exhibitions')
    rejected_at = MonitorField(monitor='verify_status', when=['rejected'], blank=True, null=True, default=None)
    rejected_by = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.SET_NULL,
                                    related_name='rejected_exhibitions')
    rejected_reason = models.TextField(default=None, blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def cover_link(self):
        return self.cover.url if self.cover else ''

    @property
    def cover_s_link(self):
        return self.cover_s.url if self.cover_s else ''

    @property
    def days_left(self):
        return (self.end_at_local - datetime.now()).days

    @property
    def start_at_local(self):
        return make_naive(self.start_at)

    @property
    def end_at_local(self):
        return make_naive(self.end_at)

    @property
    def is_end(self):
        return make_aware(datetime.now()) >= self.end_at

    @property
    def works(self):
        return list(Work.objects.filter(exhibition=self))

    @classmethod
    def retrieve_all(cls):
        return cls.objects.filter(
            status=cls.STATUS.published,
            end_at__gte=make_aware(datetime.now())
        ).order_by('-start_at', 'display_order')

    @classmethod
    def retrieve_by_space(cls, space_id: str, is_end: bool = False):
        queryset = cls.objects.filter(
            space_id=space_id,
            status=cls.STATUS.published,
            # end_at__gte=make_aware(datetime.now())
        ).order_by('-start_at', 'display_order')
        if not is_end:
            queryset = queryset & cls.objects.filter(end_at__gte=make_aware(datetime.now()))
        else:
            queryset = queryset & cls.objects.filter(end_at__lt=make_aware(datetime.now()))
        return queryset

    @classmethod
    def retrieve_by_space_as_storekeeper(cls, space_id: str):
        queryset = cls.objects.filter(
            space_id=space_id,
            status=cls.STATUS.published,
        ).order_by('-start_at', 'display_order')
        return queryset


class Work(BaseModel):
    title = models.CharField(max_length=255)
    # 750 width, in detail
    cover = models.ImageField(upload_to=upload_to)
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, default=None)
    STATUS = Choices('on', 'offline')
    status = StatusField(choices_name='STATUS', default=STATUS.offline)
    status_text = models.CharField(max_length=100)
    intro = models.CharField(max_length=2000, blank=True, default='')
    size = models.CharField(max_length=100, blank=True, default='')
    copyright = models.CharField(max_length=100, blank=True, default='')
    inventory = models.IntegerField(default=0)

    exhibition = models.ForeignKey(Exhibition, on_delete=models.SET_NULL, blank=True, null=True, default=None)

    def __str__(self):
        return self.title

    @property
    def cover_link(self):
        return self.cover.url if self.cover else ''


class Config(BaseModelSoftDeletable):
    key = models.CharField(max_length=255)
    value = models.JSONField(default=dict)

    def __str__(self):
        return self.key


class MessageThread(BaseModel):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='msg_send_thread')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='msg_received_thread')
    type = models.CharField(max_length=20, default='sys')
    object_type = models.CharField(max_length=20, default='', blank=True)
    object_id = models.CharField(max_length=20, default='', blank=True)
    is_read = models.BooleanField(default=False)
    latest_msg_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.sender.name} -> {self.receiver.name}"

    @classmethod
    def retrieve_by_receiver(cls, receiver_id):
        return cls.objects.filter(receiver_id=receiver_id).order_by('-created')

    def conversation(self):
        msg = list(self.messages.all()[:100])
        reverse_thread = MessageThread.objects.filter(sender__id=self.receiver_id, receiver_id=self.sender_id).first()
        if reverse_thread:
            msg += list(reverse_thread.messages.all()[:100])
        return sorted(msg, key=lambda x: x.created)

    def make_read(self):
        self.is_read = True
        self.save()
        Message.objects.filter(thread=self, is_read=False).update(is_read=True)


class Message(BaseModel):
    thread = models.ForeignKey(MessageThread, on_delete=models.CASCADE, related_name='messages')
    title = models.CharField(max_length=255, default='', blank=True)
    content = models.TextField(default='')
    MSG_TYPES = Choices('text', 'space_approved', 'space_rejected')
    msg_type = StatusField(choices_name='MSG_TYPES', default=MSG_TYPES.text)
    object_type = models.CharField(max_length=20, default='', blank=True)
    object_id = models.CharField(max_length=20, default='', blank=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.thread}"


@receiver(post_save, sender=Message)
def after_message_saved(sender, instance=None, created=False, **kwargs):
    if created:
        instance.thread.latest_msg_at = datetime.now()
        instance.thread.is_read = False
        instance.thread.save()


@receiver(post_save, sender=Space)
def after_space_verify_rejected(sender, instance=None, created=False, **kwargs):
    if not created:
        changes = instance.tracker.changed()
        if instance.storekeeper and instance.verify_status == 'rejected' and 'verify_status' in changes:
            sys = User.objects.get(openid='sys')
            thread, _ = MessageThread.objects.get_or_create(
                sender=sys,
                receiver=instance.storekeeper,
                type='sys'
            )
            msg = Message(
                thread=thread,
                title=f'很遗憾，你的空间【{instance.title}】未通过审核',
                content=instance.rejected_reason,
                msg_type=Message.MSG_TYPES.space_rejected,
                object_type='space',
                object_id=instance.id
            )
            msg.save()
