from django.contrib.auth import views
from django.urls import path
from .views import *

urlpatterns = [
    path('', views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('tt/update/', update_tt, name='update_tt'),
    path('hierarchy/update/', update_hierarchy, name='update_hierarchy'),
]

