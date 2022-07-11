from django.contrib import admin
from .models import Config, Link, LinkType, Banner, Space, WorkSpace, WorkSpacePosition, TaggedThrough, \
    Exhibition, Work, SpacePicture, Message, MessageThread
from django.utils.safestring import mark_safe


@admin.register(Config, Link, LinkType, Banner, WorkSpace, WorkSpacePosition, TaggedThrough, Exhibition, Work)
class CommonAdmin(admin.ModelAdmin):
    pass


class SpacePictureAdmin(admin.StackedInline):
    model = SpacePicture
    extra = 0
    readonly_fields = ['pic_img']

    @admin.display(description='Pic')
    def pic_img(self, obj):
        div = f"<img src='{obj.src}' />"
        return mark_safe(div)


@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    readonly_fields = ('storekeeper', 'accepted_by')
    inlines = (SpacePictureAdmin, )
    fieldsets = [
        ('基础信息', {'fields': ['title', 'cover', 'cover_img', 'cover_s', 'cover_s_img', 'storekeeper']}),
        ('状态', {'fields': ['status', 'published_at', 'display_order', 'favorite_count']}),
        ('审核状态', {'fields': ['verify_status', 'accepted_at', 'accepted_by', 'rejected_at', 'rejected_by', 'rejected_reason']}),
        ('地址信息', {'fields': ['address', 'province', 'city', 'district', 'longitude', 'latitude']}),
        ('介绍信息', {'fields': ['intro', 'opentime_from', 'opentime_to', 'contact_cellphone', 'space_area', 'tags']}),
    ]
    readonly_fields = ['cover_img', 'cover_s_img', 'longitude', 'latitude', 'favorite_count', 'published_at',
                       'storekeeper', 'accepted_at', 'accepted_by', 'rejected_at', 'rejected_by']

    def cover_img(self, obj):
        div = f"<img src='{obj.cover_link}' />"
        return mark_safe(div)

    def cover_s_img(self, obj):
        div = f"<img src='{obj.cover_s_link}' />"
        return mark_safe(div)


class MessageAdmin(admin.StackedInline):
    model = Message
    extra = 0


@admin.register(MessageThread)
class MessageThreadAdmin(admin.ModelAdmin):
    readonly_fields = ('latest_msg_at', )
    inlines = [MessageAdmin]
