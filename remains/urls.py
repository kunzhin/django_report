from django.urls import path

from .views import *

urlpatterns = [
    path('update/', update_remains, name='update_remains'),
    path('', remains_list, name='remains_list'),
    path('sku/', sku_move, name='sku_move'),
    path('xlsx/', xlsx, name='xlsx'),
]