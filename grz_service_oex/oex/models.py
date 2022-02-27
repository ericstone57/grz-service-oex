import urllib
from datetime import datetime

import requests
from django.db import models
from django.utils.timezone import make_naive, make_aware
from django.utils.translation import ugettext_lazy as _
from ks_shared.django.model_utils import BaseModel, upload_to, BaseModelSoftDeletable
from model_utils import Choices
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
        return self.pic.url if self.pic else ''

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
    cover = models.ImageField(upload_to=upload_to, blank=True, null=True, default=None)
    # 190 x 190, in list
    cover_s = models.ImageField(upload_to=upload_to, blank=True, null=True, default=None)

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
    VERIFY_STATUS = Choices('apply', 'rejected', 'accepted')
    verify_status = StatusField(choices_name='VERIFY_STATUS', default=VERIFY_STATUS.apply)
    accepted_at = models.DateTimeField(blank=True, null=True, default=None)
    accepted_by = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.SET_NULL,
                                    related_name='accepted_by', related_query_name='accepted_by')

    def __str__(self):
        return self.title

    def clean(self):
        if self.address:
            url = f'https://restapi.amap.com/v3/geocode/geo?key=1697dbb014867c3a2e52da21340975da&address={urllib.parse.quote_plus(self.address)}'
            resp = requests.get(url).json()
            if resp['status'] == '1':
                print(resp)
                location = resp['geocodes'][0]['location'].split(',')
                self.province = resp['geocodes'][0]['province']
                self.city = resp['geocodes'][0]['city']
                self.longitude = location[0]
                self.latitude = location[1]

    @property
    def cover_link(self):
        return self.cover.url if self.cover else ''

    @property
    def cover_s_link(self):
        return self.cover_s.url if self.cover_s else ''

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

    @classmethod
    def retrieve_all(cls):
        return cls.objects.filter(status=cls.STATUS.published).order_by('display_order', '-modified')

    @classmethod
    def retrieve_storekeeper_status(cls, user_id):
        q = cls.objects.filter(storekeeper_id=user_id)
        if q.filter(verify_status=cls.VERIFY_STATUS.accepted).count():
            return 'normal'
        if q.count():
            return 'applied'
        return 'not yet'


class SpacePicture(BaseModel):
    CATEGORY_STATUS = Choices('outside', 'inside', 'other')
    category = StatusField(choices_name='CATEGORY_STATUS', default=CATEGORY_STATUS.outside)
    file = models.FileField(upload_to=upload_to)
    space = models.ForeignKey(Space, on_delete=models.CASCADE)


class WorkSpace(BaseModel):
    title = models.CharField(max_length=255)
    # 555 x 380
    cover = models.ImageField(upload_to=upload_to)

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
