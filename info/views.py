from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from .models import Info


# Create your views here.


class ViewInfoList(LoginRequiredMixin, ListView):
    login_url = '/'
    model = Info
    context_object_name = 'info_list'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Информация'
        return context

    def get_queryset(self):
        return Info.objects.all()


class ViewInfoDetail(LoginRequiredMixin, DetailView):
    login_url = '/'
    model = Info
    context_object_name = 'info_detail'
