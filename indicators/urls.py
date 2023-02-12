from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='indicators'),
    path('sidebar_filter/', sidebar_filter, name='sidebar_filter'),
    path('history_tt/', history_tt, name = 'history_tt'),
    path('update07/', update_07_report, name='update_07_report'),
    path('update145/', update_145_report, name='update_145_report'),
    path('update770/', update_770_report, name='update_770_report'),
    path('update_plan/', update_volume_plan, name='update_volume_plan'),
    path('terr_filter/', territory_filter, name='territory_filter'),
    path('volume/', volume, name='volume'),
    path('topx/', topx, name='topx'),
    path('coverage/', coverage, name='coverage'),
    path('info_tt/', info_tt, name='info_tt'),
    path('strength/', task, name='task'),
]
