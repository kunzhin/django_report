from django.contrib import admin
from django.contrib.admin import filters
from .models import *
# Register your models here.


class InfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'photo', 'is_published', 'is_fixed')


admin.site.register(Info, InfoAdmin)
