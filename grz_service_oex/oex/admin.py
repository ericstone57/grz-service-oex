from django.contrib import admin
from .models import Config, Link, LinkType, Banner, Space, WorkSpace, WorkSpacePosition, TaggedThrough, Exhibition, Work


@admin.register(Config, Link, LinkType, Banner, Space, WorkSpace, WorkSpacePosition, TaggedThrough, Exhibition, Work)
class CommonAdmin(admin.ModelAdmin):
    pass
