import simplejson as simplejson
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from pytz import unicode
from .models import PhotostreamForm
from .forms import PhotostreamInsertForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from accounts.models import ESR, TSM, DSM, Address, TT
from django.http import HttpResponse
from .func_photostream import photostream_status_df, data_statistics_df
from indicators.func import df_to_html
from report_audit_control.date_work import time_passed

import pandas as pd


@login_required(login_url='/')
def index(request):
    context = {'title': 'Фотопоток'}

    return render(request, template_name='photostream/index.html', context=context)


@login_required(login_url='/')
def territory_filter(request):
    dsm = request.GET.get('dsm')
    tsm = request.GET.get('tsm')
    if dsm:
        tsm = TSM.objects.filter(dsm_id__dsm=dsm)
        context = {
            'tsm': tsm
        }
        return render(request, template_name='indicators/inc/_tsm.html', context=context)

    if tsm:
        esr = ESR.objects.filter(tsm_id__tsm=tsm)
        context = {
            'esr': esr
        }
        return render(request, template_name='indicators/inc/_esr.html', context=context)


@login_required(login_url='/')
def data_statistics(request):
    dsm = request.GET.get('dsm')
    tsm = request.GET.get('tsm')
    esr = request.GET.get('esr')
    start_day = request.GET.get('start_day')
    end_day = request.GET.get('end_day')

    if dsm:
        if dsm == 'КОНТИНЕНТ':
            data = PhotostreamForm.objects.filter(created_at__range=(start_day, end_day)
                                                  ).values('dsm__dsm',
                                                           'tsm__tsm',
                                                           'esr__esr',
                                                           'address',
                                                           'category__name',
                                                           'status_worked_out',
                                                           'created_at')
            audit = PhotostreamForm.objects.filter(created_at__range=(start_day, end_day),
                                                   )
            df_dsm = df_to_html(photostream_status_df(data)[0], 'photostream_result')
            df_tsm = df_to_html(photostream_status_df(data)[1], 'photostream_result')

            context = {'df_dsm': df_dsm,
                       'df_tsm': df_tsm,
                       'dsm': dsm,
                       'audit': audit,
                       }

            return render(request, template_name='photostream/data_audit.html', context=context)

        elif dsm == 'Кузбасс - Алтай':
            value, param_user = ('GC_Кузбасс_DSM', 'GC_Алтай_DSM'), 'dsm_id__dsm'

        else:
            value, param_user, = dsm, 'dsm_id__dsm'

    elif tsm:
        value, param_user = tsm, 'tsm_id__tsm'

    elif esr:
        value, param_user = esr, 'esr_id__esr'

    data = PhotostreamForm.objects.filter(**{param_user: value}, created_at__range=(start_day, end_day),
                                          ).values(param_user,
                                                   'address',
                                                   'category__name',
                                                   'status_worked_out',
                                                   'created_at')

    audit = PhotostreamForm.objects.filter(**{param_user: value}, created_at__range=(start_day, end_day))

    if data:
        category_df = df_to_html(data_statistics_df(data)[0], 'category_df')
        data_df = df_to_html(data_statistics_df(data)[1], 'data_df')

        context = {'title': 'Статистика',
                   'dsm': dsm,
                   'tsm': tsm,
                   'esr': esr,
                   'category_df': category_df,
                   'data_df': data_df,
                   'audit': audit,
                   }

        return render(request, template_name='photostream/data_audit.html', context=context)

    else:
        context = {'title': 'Статистика',
                   'empty': 'Нет данных!'}

        return render(request, template_name='photostream/data_audit.html', context=context)


@login_required(login_url='/')
def statistics(request):
    context = {'title': 'Статистика',
               'dsm': DSM.objects.all(),
               'time': time_passed()}

    return render(request, template_name='photostream/statistics.html', context=context)


# Заполнение формы территориями
@login_required(login_url='/')
def parent_to_children(request):
    global ret
    esr_id = request.GET.get('id_esr')
    tt_id = request.GET.get('id_tt')

    if request.user.userprofile.tsm.id:
        tsm_id = request.user.userprofile.tsm.id
        ret = []
        for esr in ESR.objects.filter(tsm=tsm_id):
            ret.append(dict(id=esr.id, value=unicode(esr)))

    if esr_id:
        ret = []
        for tt in TT.objects.filter(esr=esr_id):
            ret.append(dict(id=tt.id, value=unicode(tt)))

    if tt_id:
        ret = []
        for address in Address.objects.filter(tt=tt_id):
            ret.append(dict(id=address.id, value=unicode(address)))

    if len(ret) != 1:
        ret.insert(0, dict(id='', value='Выбери'))

    return HttpResponse(simplejson.dumps(ret), content_type='application/json')


# Список проведенных аудитов фотопотока
class ViewPhotostreamAuditList(LoginRequiredMixin, ListView):
    login_url = '/'
    model = PhotostreamForm
    context_object_name = 'audit_item_list'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список аудитов'
        return context

    def get_queryset(self):
        if self.request.user.groups.filter(name='ESR').exists():
            return PhotostreamForm.objects.filter(
                esr__esr=self.request.user.userprofile.esr
            ).order_by(
                'status_worked_out',
                'date_correction',
                '-created_at'
            )
        if self.request.user.groups.filter(name='TSM').exists():
            return PhotostreamForm.objects.filter(
                tsm__tsm=self.request.user.userprofile.tsm
            ).order_by(
                'status_worked_out',
                'date_correction',
                '-created_at'
            )
        if self.request.user.groups.filter(name='DSM').exists():
            return PhotostreamForm.objects.filter(
                dsm__dsm=self.request.user.userprofile.dsm
            ).order_by(
                'status_worked_out',
                'date_correction',
                '-created_at'
            )
        else:
            return PhotostreamForm.objects.all().order_by(
                '-created_at'
            )


# Детальное отображение аудита
class ViewPhotostreamAudit(LoginRequiredMixin, DetailView):
    login_url = '/'
    model = PhotostreamForm
    context_object_name = 'audit_item'


# Форма записи аудита в модель
class CreatePhotostreamRecord(LoginRequiredMixin, CreateView):
    login_url = '/'
    form_class = PhotostreamInsertForm
    template_name = 'photostream/add_photostream_audit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить аудит'
        return context

    # UserPassesTestMixin Если юзер в группе ESR блокируем доступ
    # def test_func(self):
    #     return self.request.user.groups.filter(name='TSM').exists()


# Форма записи полевого аудита в модель
class CreateFieldPhotostreamRecord(LoginRequiredMixin, CreateView):
    login_url = '/'
    model = PhotostreamForm
    fields = ['photo', 'category']
    template_name = 'photostream/add_photostream_field_audit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить аудит'
        return context


# Форма обновления статуса аудита
class UpdatePhotostreamAudit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = '/'
    model = PhotostreamForm
    context_object_name = 'audit_item'
    fields = ['status_worked_out']
    template_name = 'photostream/edit_photostream_audit.html'

    # UserPassesTestMixin Если юзер в группе ESR блокируем доступ
    def test_func(self):
        return self.request.user.groups.filter(name='TSM').exists()


# Форма загрузки исправленного фото
class UpdatePhotoAudit(LoginRequiredMixin, UpdateView):
    login_url = '/'
    model = PhotostreamForm
    context_object_name = 'audit_item'
    fields = ['photo']
    template_name = 'photostream/edit_photo_audit.html'
