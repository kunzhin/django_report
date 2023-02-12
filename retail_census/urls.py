from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='census'),
    path('add_outlet_record/', RecordOutletInfo.as_view(), name='add_outlet_record'),
    path('outlet_list/', ViewOutletList.as_view(), name='outlet_list'),
    path('retailcensus/<int:pk>/', ViewOutlet.as_view(), name='view_outlet'),
    path('add_outlet_record/json/', parent_to_children, name='json')
]