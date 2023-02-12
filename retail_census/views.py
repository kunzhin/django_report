from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from retail_census.models import Outlet
from .forms import OutletInsertForm
from accounts.models import ESR
from pytz import unicode
import simplejson as simplejson
from django.http import HttpResponse
from django.shortcuts import reverse


# Create your views here.


@login_required(login_url='/')
def index(request):
    context = {'title': 'Сенсус'}

    return render(request, template_name='retail_census/index.html', context=context)


class RecordOutletInfo(LoginRequiredMixin, CreateView):
    login_url = '/'
    form_class = OutletInsertForm
    template_name = 'retail_census/addOutlet.html'
    success_url = '/retailcensus/outlet_list/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить запись'
        return context


class ViewOutlet(LoginRequiredMixin, DetailView):
    login_url = '/'
    model = Outlet
    context_object_name = 'outlet_item'
    template_name = 'retail_census/modalDetail.html'


class ViewOutletList(LoginRequiredMixin, ListView):
    login_url = '/'
    model = Outlet
    context_object_name = 'outlet_list'
    template_name= 'retail_census/outletList.html'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список потенциальных точек'
        return context

    def get_queryset(self):
        if self.request.user.groups.filter(name='ESR').exists():
            return Outlet.objects.filter(
                esr__esr=self.request.user.userprofile.esr
            )
        if self.request.user.groups.filter(name='TSM').exists():
            return Outlet.objects.filter(
                tsm__tsm=self.request.user.userprofile.tsm
            )
        if self.request.user.groups.filter(name='DSM').exists():
            return Outlet.objects.filter(
                dsm__dsm=self.request.user.userprofile.dsm
            )
        else:
            return Outlet.objects.all()


# Заполнение формы территориями
@login_required(login_url='/')
def parent_to_children(request):
    try:
        if request.user.userprofile.esr.id:
            ret = []
            ret.append(dict(id=request.user.userprofile.esr.id, 
                            value=unicode(request.user.userprofile.esr)))
    except AttributeError:
        try:
            if request.user.userprofile.tsm.id:
                ret = []
                for esr in ESR.objects.filter(tsm=request.user.userprofile.tsm.id):
                    ret.append(dict(id=esr.id, value=unicode(esr)))

                if len(ret) != 1:
                    ret.insert(0, dict(id='', value='Выбери'))
        except AttributeError:
            try:
                if request.user.userprofile.dsm.id:
                    ret = []
                    for esr in ESR.objects.filter(tsm__dsm_id__dsm=request.user.userprofile.dsm):
                        ret.append(dict(id=esr.id, value=unicode(esr)))

                    if len(ret) != 1:
                        ret.insert(0, dict(id='', value='Выбери'))
            except AttributeError:
                ret = []
                for esr in ESR.objects.all():
                    ret.append(dict(id=esr.id, value=unicode(esr)))

                if len(ret) != 1:
                    ret.insert(0, dict(id='', value='Выбери'))

    return HttpResponse(simplejson.dumps(ret), content_type='application/json')