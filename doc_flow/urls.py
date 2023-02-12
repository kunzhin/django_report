from django.urls import path

from .views import *


urlpatterns = [
    path('', doc_flow, name='doc_flow'),
]