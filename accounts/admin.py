from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import *


class UserInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Доп. информация'


# Определяем новый класс настроек для модели User
class UserAdmin(UserAdmin):
    inlines = (UserInline,)


class DSMAdmin(admin.ModelAdmin):
    list_display = ('dsm',)
    search_fields = ('dsm',)


class TSMAdmin(admin.ModelAdmin):
    list_display = ('tsm', 'dsm')
    search_fields = ('tsm', 'dsm__dsm')


class ESRAdmin(admin.ModelAdmin):
    list_display = ('esr', 'tsm')
    search_fields = ('esr', 'tsm__tsm')


class TTAdmin(admin.ModelAdmin):
    list_display = ('tt', 'esr')
    search_fields = ('tt', 'esr__esr')


class AddressAdmin(admin.ModelAdmin):
    list_display = ('tt', 'address')
    search_fields = ('tt__tt', 'address')


class HierarchyAdmin(admin.ModelAdmin):
    list_display = ('dsm', 'tsm', 'esr')
    search_fields = ('dsm', 'tsm', 'esr')


# Перерегистрируем модель User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(DSM, DSMAdmin)
admin.site.register(TSM, TSMAdmin)
admin.site.register(ESR, ESRAdmin)
admin.site.register(TT, TTAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Hierarchy, HierarchyAdmin)
