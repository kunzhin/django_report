from django.contrib import admin
from django.contrib.admin import filters
from .models import *

# Register your models here.

class OutletAdmin(admin.ModelAdmin):
    list_display= ('dsm', 
                    'tsm', 
                    'esr', 
                    'corporateBodyName', 
                    'taxIdentificationNumber',
                    'count_tt',
                    'deliveryContract',
                    'statusWorkedOut')
    
    search_fields= ('dsm', 
                    'tsm', 
                    'esr', 
                    'corporateBodyName', 
                    'taxIdentificationNumber',
                    'count_tt',
                    'deliveryContract',
                    'statusWorkedOut')
    
    filters= ('dsm', 
                    'tsm', 
                    'esr', 
                    'corporateBodyName', 
                    'taxIdentificationNumber',
                    'count_tt',
                    'deliveryContract',
                    'statusWorkedOut')

    ordering = ('-created_at', )


class PrePresenceNestleAdmin(admin.ModelAdmin):
    list_display= ('presenceNestle',)


class CompetitorsAdmin(admin.ModelAdmin):
    list_display= ('competitors',)


admin.site.register(Outlet, OutletAdmin)
admin.site.register(PresenceNestle, PrePresenceNestleAdmin)
admin.site.register(Competitors, CompetitorsAdmin)