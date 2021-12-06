from django.contrib import admin
from .models import User, Config


@admin.register(User, Config)
class CommonAdmin(admin.ModelAdmin):
    pass
