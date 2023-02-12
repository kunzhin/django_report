from django.contrib import admin
from django.http import HttpResponseRedirect

from .models import *
from django.contrib.admin import filters

# Register your models here.


class LaunchAdmin(admin.ModelAdmin):
    list_display = ('dbc', 'code_nestle', 'dbc_name')


class CategoryRemainsAdmin(admin.ModelAdmin):
    list_display = ('code_category', 'category',)


class RemainsAdmin(admin.ModelAdmin):

    list_display = ('category',
                    'nomenclature',
                    'expiration_date',
                    )

    search_fields = ('category',
                     'nomenclature',
                     'expiration_date',
                     'date_arrival',
                     )

    filters = ('category',
               'nomenclature',
               'expiration_date',
               'date_arrival',
               )


admin.site.register(Remains, RemainsAdmin)
admin.site.register(CategoryRemains, CategoryRemainsAdmin)
admin.site.register(Launch, LaunchAdmin)
admin.site.register(RemainsFile)

