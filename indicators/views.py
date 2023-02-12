from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, JsonResponse
import pandas as pd
import numpy as np
import time

from .update_report import update_07, update_145, update_770
from .update_plan import update_plan
from .func import df_plan_tsm, df_topx, df_coverage, df_to_html, tt_info, get_excel_file
from .func import HistoryTT, UserTask
from accounts.models import DSM, TSM, ESR, Address
from .models import *
from report_audit_control.date_work import time_passed


from datetime import datetime


# Create your views here.
@login_required(login_url='/')
def task(request):
    dsm = request.GET.get('dsm')
    tsm = request.GET.get('tsm')
    esr = request.GET.get('esr')

    if dsm:
        if dsm == 'КОНТИНЕНТ':
            territory, user = 'GC_Сибирь_Континент_SM', 'rsm'

        elif dsm == 'Кузбасс - Алтай':
            territory, user = ('GC_Кузбасс_DSM', 'GC_Алтай_DSM'), 'dsm__in'

        else:
            territory, user = dsm, 'dsm'

    elif tsm:
        territory, user = tsm, 'tsm'

    elif esr:
        territory, user = esr, 'esr'

    data = UserTask(territory, user)

    context = {
        'title': 'Запуски',
        'dsm': dsm,
        'tsm': tsm,
        'esr': esr,
        'df_task': df_to_html(data.result(), 'task'),
        'coffee_nan': df_to_html(data.foto_nan('Coffee'), 'coffee_nan'),
        'maggi_nan': df_to_html(data.foto_nan('Maggi'), 'maggi_nan'),
        'purina_nan': df_to_html(data.foto_nan('Purina'), 'purina_nan'),
        'coffee_nan_count': len(data.foto_nan('Coffee')),
        'maggi_nan_count': len(data.foto_nan('Maggi')),
        'purina_nan_count': len(data.foto_nan('Purina')),
        'launches': df_to_html(data.launches(), 'launch'),
    }

    return render(request, template_name='indicators/task.html', context=context)


@login_required(login_url='/')
def history_tt(request):
    user = request.GET.get('user')
    territory = request.GET.get('territory')
    name_tt = request.GET.get('name_tt')
    address = request.GET.get('address')

    data_tt = HistoryTT(user, territory, name_tt, address)
    try:
        context = {
            'name_tt': name_tt,
            'channel': data_tt.channel(),
            'last_date_shipment': str(data_tt.last_date_shipment()),
            'chain': data_tt.network(),
            'avg_num_orders': str(data_tt.avg_num_orders()),
            'topx': df_to_html(data_tt.topx(), 'topx_table'),
            'volume': df_to_html(data_tt.volume(), 'volume_table'),
            'purina_strenght': data_tt.purina_strenght(),
            'maggi_strenght': data_tt.maggi_strenght(),
            'coffee_strength': data_tt.coffee_strength(),
            'foto': data_tt.fotostream()
        }

    except Exception as error:

        context = {
            'error': error,
            'no_data': 'Нет данных!'
        }

    return render(request, template_name='indicators/inc/_modal_history.html', context=context)


@login_required(login_url='/')
def index(request):
    context = {
        'title': 'Показатели',
        'date_update': ReportFile.objects.last()
    }
    return render(request, template_name='indicators/index.html', context=context)


@login_required(login_url='/')
def volume(request):
    dsm = request.GET.get('dsm')
    tsm = request.GET.get('tsm')
    esr = request.GET.get('esr')
    start_day = request.GET.get('start_day')
    end_day = request.GET.get('end_day')

    if dsm:
        if dsm == 'КОНТИНЕНТ':
            value, param_user = 'GC_Сибирь_Континент_SM', 'rsm'
            volume_plan = pd.DataFrame(VolumePlanTSM.objects.all().values())

        elif dsm == 'Кузбасс - Алтай':
            value, param_user = ('GC_Кузбасс_DSM', 'GC_Алтай_DSM'), 'dsm__in'
            volume_plan = pd.DataFrame(VolumePlanTSM.objects.filter(**{param_user: value}).values())

        else:
            value, param_user = dsm, 'dsm'
            volume_plan = pd.DataFrame(VolumePlanTSM.objects.filter(**{param_user: value}).values())

    elif tsm:
        value, param_user = tsm, 'tsm'
        volume_plan = pd.DataFrame(VolumePlanTSM.objects.filter(**{param_user: value}).values())

    elif esr:
        value, param_user = esr, 'esr'
        volume_plan = pd.DataFrame(VolumePlanESR.objects.filter(**{param_user: value}).values())

    volume_fact = pd.DataFrame(Report07.objects.filter(**{param_user: value},
                                                       date_shipment__range=(start_day, end_day),
                                                       stream_tk='Традиция'
                                                       ).values('tier',
                                                                'rev_group',
                                                                'rev_pre_group',
                                                                'sum_sell'))
    # Меняем Tier2 в традиции на Tier TT
    try:
        volume_fact['tier'] = np.where(volume_fact['tier'] == 'Tier 2', 'Tier TT', volume_fact['tier'])
    except KeyError:
        pass

    volume_plan['TOTAL'] = 'TOTAL'
    volume_fact['TOTAL'] = 'TOTAL'

    tier = ['TOTAL', 'Tier3', 'TierTT', 'TierWHS', 'KeyWHS']

    df = df_plan_tsm(volume_plan, volume_fact)

    dict_df = {name: df_to_html(df_table, 'volume_table') for name, df_table in zip(tier, df)}

    context = {
        'title': 'Объем',
        'dsm': dsm,
        'tsm': tsm,
        'esr': esr,
    }

    context.update(dict_df)

    return render(request, template_name='indicators/volume.html', context=context)


@login_required(login_url='/')
def topx(request):
    dsm = request.GET.get('dsm')
    tsm = request.GET.get('tsm')
    esr = request.GET.get('esr')
    start_day = request.GET.get('start_day')
    end_day = request.GET.get('end_day')
    cat_topx = pd.DataFrame(TopCategory.objects.all().values('dbc', 'dbc_name', 'min_sell'))

    if dsm:
        if dsm == 'КОНТИНЕНТ':
            value, param_user = 'GC_Сибирь_Континент_SM', 'rsm'

        elif dsm == 'Кузбасс - Алтай':
            value, param_user = ('GC_Кузбасс_DSM', 'GC_Алтай_DSM'), 'dsm__in'

        else:
            value, param_user = dsm, 'dsm'

    elif tsm:
        value, param_user = tsm, 'tsm'

    elif esr:
        value, param_user = esr, 'esr'

    if value == 'GC_Сибирь_Континент_SM':
        topx_plan = pd.DataFrame(TopPlan.objects.all().values())
    else:
        topx_plan = pd.DataFrame(TopPlan.objects.filter(**{param_user: value}).values())

    topx_fact = pd.DataFrame(Report07.objects.filter(**{param_user: value},
                                                     date_shipment__range=(start_day, end_day),
                                                     stream_tk='Традиция'
                                                     ).exclude(channel_tt='Wholesalers'
                                                               ).values('code_tt_kis',
                                                                        'rev_group_top',
                                                                        'dbc',
                                                                        'dbc_name',
                                                                        'count_piece')).dropna()

    df = df_topx(topx_plan, topx_fact, cat_topx)

    df = df_to_html(df, 'topx_table')

    context = {
        'title': 'Объем',
        'dsm': dsm,
        'tsm': tsm,
        'esr': esr,
        'df_topx': df,
    }

    return render(request, template_name='indicators/topx.html', context=context)


@login_required(login_url='/')
def coverage(request):
    dsm = request.GET.get('dsm')
    tsm = request.GET.get('tsm')
    esr = request.GET.get('esr')
    start_day = request.GET.get('start_day')
    end_day = request.GET.get('end_day')

    if dsm:
        if dsm == 'КОНТИНЕНТ':
            value, param_user, param_list, user = ('GC_Кузбасс_DSM', 'GC_Алтай_DSM', 'GC_Красноярск_DSM',
                                                   'GC_KO_Продажи_Нск_Томск_DSM',
                                                   'GC_KO_Омск_DSM'), 'dsm__in', 'tt__esr__tsm__dsm_id__dsm__in', 'dsm'

        elif dsm == 'Кузбасс - Алтай':
            value, param_user, param_list, user = ('GC_Кузбасс_DSM',
                                                   'GC_Алтай_DSM'), 'dsm__in', 'tt__esr__tsm__dsm_id__dsm__in', 'dsm'

        else:
            value, param_user, param_list, user = dsm, 'dsm', 'tt__esr__tsm__dsm_id__dsm', 'dsm'

    elif tsm:
        value, param_user, param_list, user = tsm, 'tsm', 'tt__esr__tsm_id__tsm', 'tsm'

    elif esr:
        value, param_user, param_list, user = esr, 'esr', 'tt__esr_id__esr', 'esr'
    '''
    if value == 'GC_Сибирь_Континент_SM':
        tt_list = pd.DataFrame(
            Address.objects.all().values('kis_code', 'address', 'tt_id__tt')).drop_duplicates()

        cov_plan = pd.DataFrame(CoveragePlan.objects.all().values(param_user, 'target'))
    '''

    tt_list = pd.DataFrame(
        Address.objects.filter(**{param_list: value}).values('kis_code', 'address', 'tt_id__tt')).drop_duplicates()

    cov_plan = pd.DataFrame(CoveragePlan.objects.filter(**{param_user: value}).values(user, 'target'))

    cov_fact = pd.DataFrame(Report07.objects.filter(**{param_user: value},
                                                    date_shipment__range=(start_day, end_day),
                                                    stream_tk='Традиция'
                                                    ).values(user, 'code_tt_kis', 'sum_sell'))

    if cov_plan.empty and cov_fact.empty:
        df_cov = df_to_html(pd.DataFrame(columns=['Территория', 'План', 'Факт', '%', 'Осталось', 'План на день']),
                            'coverage_table')

        df_tt = df_to_html(pd.DataFrame(columns=['Наименование ТТ', 'Адрес ТТ', 'Сумма продаж']), 'coverage_tt_table')

        dont_work = 0
    else:
        df = df_coverage(cov_plan, cov_fact, user, tt_list)

        df_cov = df_to_html(df[0], 'coverage_table')

        df_tt = df_to_html(df[1], 'coverage_tt_table')

        dont_work = len(df[1].index)

    context = {
        'title': 'Покрытие',
        'dsm': dsm,
        'tsm': tsm,
        'esr': esr,
        'df_coverage': df_cov,
        'df_tt': df_tt,
        'dont_work': dont_work,
    }

    return render(request, template_name='indicators/coverage.html', context=context)


@login_required(login_url='/')
def info_tt(request):
    if request.method == 'GET':
        tsm = request.GET.get('tsm')
        esr = request.GET.get('esr')

        if tsm:
            value, param_user, param_list = tsm, 'tsm', 'tt__esr__tsm_id__tsm'

        if esr:
            value, param_user, param_list = esr, 'esr', 'tt__esr_id__esr'

        tt_list = pd.DataFrame(
            Address.objects.filter(**{param_list: value}).values('code_tt', 'kis_code', 'tt_id__tt', 'address',
                                                                 'day_route')).drop_duplicates()
        if not tt_list.empty:
            df_info = tt_info(tt_list, value, param_user)

            img = ['tt-name.png', 'Address.png', 'CalendarPlus.png',
                   'Sigma.png', 'coffee_beans_24px.png', 'pepper_grinder_24px.png', 'pets_24px.png', 'Camera.png']

            context = {
                'title': 'Информация по ТТ',
                'tsm': tsm,
                'esr': esr,
                'df_info': df_info,
                'img': img,
            }

            return render(request, template_name='indicators/info_tt.html', context=context)

        else:
            return JsonResponse({'message': 'Нет продаж за последние 3мес'})

    elif request.method == 'POST':
        data = request.POST

        if data['dsm'] == 'КОНТИНЕНТ':
            value, param_user = 'GC_Сибирь_Континент_SM', 'rsm'

        elif data['dsm'] == 'Кузбасс - Алтай':
            value, param_user, param_list = ('GC_Кузбасс_DSM',
                                             'GC_Алтай_DSM'), 'dsm__in', 'tt__esr__tsm__dsm_id__dsm__in'

        else:
            value, param_user, param_list = data['dsm'], 'dsm', 'tt__esr__tsm__dsm_id__dsm'

        if value == 'GC_Сибирь_Континент_SM':
            tt_list = pd.DataFrame(
                Address.objects.all().values('code_tt',
                                             'kis_code',
                                             'tt_id__esr_id__tsm_id__dsm_id__dsm',
                                             'tt_id__esr_id__tsm_id__tsm',
                                             'tt_id__esr_id__esr',
                                             'tt_id__tt',
                                             'address',
                                             'tier',
                                             'channel_tt',
                                             'day_route')).drop_duplicates()
        else:
            tt_list = pd.DataFrame(
                Address.objects.filter(**{param_list: value}).values('code_tt',
                                                                     'kis_code',
                                                                     'tt_id__esr_id__tsm_id__dsm_id__dsm',
                                                                     'tt_id__esr_id__tsm_id__tsm',
                                                                     'tt_id__esr_id__esr',
                                                                     'tt_id__tt',
                                                                     'address',
                                                                     'tier',
                                                                     'channel_tt',
                                                                     'day_route')).drop_duplicates()

        filename = 'Report_' + time.strftime('%d%B') + '.xlsx'  # Название файла с датой создания
        response = get_excel_file(tt_info(tt_list, value, param_user, xlsx=True), filename)

        return response

@login_required(login_url='/')
def sidebar_filter(request):
    kpi = request.GET.get('kpi')
    context = {'title': 'Объем',
               'dsm': DSM.objects.all(),
               'time': time_passed(),
               'kpi': kpi,
               }

    return render(request, template_name='indicators/inc/_territory_sidebar.html', context=context)


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


# Доступ только для администратора. Добавить возврат ошибок.
@user_passes_test(lambda u: u.is_superuser)
def update_07_report(request):
    message = request.GET.get('message')
    exec_time = update_07(message)
    return HttpResponse('Данные обновлены! Время: ' + str(exec_time))


# Доступ только для администратора. Добавить возврат ошибок.
@user_passes_test(lambda u: u.is_superuser)
def update_145_report(request):
    exec_time = update_145()
    return HttpResponse('Данные обновлены! Время: ' + str(exec_time))


@user_passes_test(lambda u: u.is_superuser)
def update_770_report(request):
    message = request.GET.get('message')
    exec_time = update_770(message)
    return HttpResponse('Данные обновлены! Время: ' + str(exec_time))


# Доступ только для администратора. Добавить возврат ошибок.
@user_passes_test(lambda u: u.is_superuser)
def update_volume_plan(request):
    message = request.GET.get('message')
    exec_time = update_plan(message)
    return HttpResponse('Данные обновлены! Время: ' + str(exec_time))
