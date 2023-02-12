from django.contrib import admin
from django.contrib.admin import filters
from .models import *
# Register your models here.


class CategoryPhotoAdmin(admin.ModelAdmin):
    list_display = ('name',)


class PhotostreamFormAdmin(admin.ModelAdmin):
    list_display = ('tsm', 'esr', 'tt', 'category', 'created_at', 'status_worked_out')
    search_fields = ('tt', 'category')
    filters = ('tsm', 'esr', 'tt', 'category', 'created_at', 'status_worked_out')


admin.site.register(CategoryPhoto, CategoryPhotoAdmin)
admin.site.register(PhotostreamForm, PhotostreamFormAdmin)