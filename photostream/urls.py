from os import name
from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='photostream'),
    path('statistics/', statistics, name='statistics'),
    path('statistics/terr_filter/', territory_filter, name='territory_filter'),
    path('statistics/data/', data_statistics, name='data_statistics'),
    path('add_photo_comment/', CreatePhotostreamRecord.as_view(), name='add_photo_comment'),
    path('add_photo_field_comment/', CreateFieldPhotostreamRecord.as_view(), name='add_photo_field_comment'),
    path('photostream/<int:pk>/edit', UpdatePhotostreamAudit.as_view(), name='edit_photostream_audit'),
    path('photostream/<int:pk>/edit_photo', UpdatePhotoAudit.as_view(), name='edit_photo_audit'),
    path('photostream_audit_list/', ViewPhotostreamAuditList.as_view(), name='photostream_audit_list'),
    path('photostream/<int:pk>/', ViewPhotostreamAudit.as_view(), name='view_photostream_audit'),
    path('add_photo_comment/json/', parent_to_children, name='json'),
    path('add_photo_field_comment/json/', parent_to_children, name='json')
]