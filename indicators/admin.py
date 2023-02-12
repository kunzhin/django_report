from django.contrib import admin
from .models import *


# Register your models here.


class VolumeCategoryAdmin(admin.ModelAdmin):
    list_display = ('group', 'rev_pre_group', 'rev_group')


class TopCategoryAdmin(admin.ModelAdmin):
    list_display = ('dbc_name', 'dbc', 'rev_group_top', 'min_sell')


class PlanFileAdmin(admin.ModelAdmin):
    list_display = ('date',)


class ReportFileAdmin(admin.ModelAdmin):
    list_display = ('date',)


class MonthAdmin(admin.ModelAdmin):
    list_display = ('month',)


class TierAdmin(admin.ModelAdmin):
    list_display = ('tier',)


class ChannelTTAdmin(admin.ModelAdmin):
    list_display = ('channel',)


class DBCNameAdmin(admin.ModelAdmin):
    list_display = ('DBC_name',)


class IdeaToLaunchAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'dbc_list', 'min_threshold', 'month_list', 'tier_list', 'channel_list', 'func_launch', 'info_tt_view')


class TaskCategoryAdmin(admin.ModelAdmin):
    list_display = ('dbc_name', 'distr_task', )


class Report770Admin(admin.ModelAdmin):
    list_display = ('date_foto', 'name_tt', 'address_tt', 'status_price', 'standart_shop', 'status',)
    search_fields = ('date_foto', 'name_tt', 'address_tt', 'status_price', 'standart_shop', 'status',)


class Report770FileAdmin(admin.ModelAdmin):
    list_display = ('date', )


admin.site.register(VolumeCategory, VolumeCategoryAdmin)
admin.site.register(TopCategory, TopCategoryAdmin)
admin.site.register(ReportFile, ReportFileAdmin)
admin.site.register(PlanFile, PlanFileAdmin)
admin.site.register(Month, MonthAdmin)
admin.site.register(Tier, TierAdmin)
admin.site.register(ChannelTT, ChannelTTAdmin)
admin.site.register(DBCName, DBCNameAdmin)
admin.site.register(IdeaToLaunch, IdeaToLaunchAdmin)
admin.site.register(TaskCategory, TaskCategoryAdmin)
admin.site.register(Report770, Report770Admin)
admin.site.register(Report770File, Report770FileAdmin)
