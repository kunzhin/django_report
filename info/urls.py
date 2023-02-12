from django.urls import path

from .views import *

urlpatterns = [
    path('', ViewInfoList.as_view(), name='info'),
    path('information/<int:pk>/', ViewInfoDetail.as_view(), name='info_item'),
]
