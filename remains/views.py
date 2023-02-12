import pandas as pd
import time
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from indicators.func import df_to_html, get_excel_file
from .func import contlog_remains, SKU
from .update_remains import update_data_remains
from .models import *



# Доступ только для администратора. Добавить возврат ошибок.
@user_passes_test(lambda u: u.is_superuser)
def update_remains(request):
    message = request.GET.get('message')
    print(message)
    time = update_data_remains(message)
    return HttpResponse('Данные обновлены! Время: ' + str(time))


@login_required(login_url='/')
def sku_move(request):

    sku_move = SKU(request.GET.get('sap'))
    sku_name = request.GET.get('sku_name')

    move = sku_move.move()

    if move is None:
        move = 'Нет движения по площадкам...'
    else:
        move = df_to_html(move, 'sku_info')

    context = {
        'sap': request.GET.get('sap'),
        'sku_move': move,
        'sku_name': sku_name,
    }
    return render(request, template_name='remains/inc/_modal_skuMove.html', context=context)

@login_required(login_url='/')
def xlsx(request):
    remains = pd.DataFrame(Remains.objects.all().values())
    remains = remains.groupby(['city',
                               'code_continent',
                               'code_nestle',
                               'category',
                               'nomenclature',
                               'reserve',
                               'free_remain',
                               'expiration_date',
                               'date_arrival',
                               'topx'
                               ]).sum(numeric_only=True).reset_index().drop(['id'], axis=1)

    filename = 'Остатки_' + time.strftime('%d%B') + '.xlsx'
    resource = get_excel_file(remains, filename, True)

    return resource


@login_required(login_url='/')
def remains_list(request):
    ajax = request.POST
    if 'id' in ajax:
        if ajax['id'] == 'kontinent':
            remains = pd.DataFrame(Remains.objects.all().values())

            df_remains = contlog_remains(remains)

            context = {'remains_contlog': df_remains,
                       'city': ajax['city'],
                       'city_id': ajax['id'],
                       'category': CategoryRemains.objects.all(),
                       'date_update': RemainsFile.objects.last()}

            return render(request, template_name='remains/remains_list.html', context=context)
        else:
            remains = Remains.objects.filter(city=ajax['id'])
            context = {'remains': remains,
                       'city': ajax['city'],
                       'city_id': ajax['id'],
                       'category': CategoryRemains.objects.all(),
                       'date_update': RemainsFile.objects.last()}

            return render(request, template_name='remains/remains_list.html', context=context)

    if 'code_category' in ajax:

        if ajax['code_category'] == 'topx':

            if ajax['city_name'] == 'kontinent':

                remains = pd.DataFrame(Remains.objects.filter(topx=ajax['code_category']).values())

                df_remains = contlog_remains(remains)

                context = {'remains_contlog': df_remains,
                           'category': CategoryRemains.objects.all()}

                return render(request, template_name='remains/remains_contlog.html', context=context)

            else:
                remains = Remains.objects.filter(city=ajax['city_name'], topx=ajax['code_category'])


        elif ajax['code_category'] == 'suspended':

            if ajax['city_name'] == 'kontinent':

                remains = pd.DataFrame(Remains.objects.filter(status=ajax['code_category']).values())

                df_remains = contlog_remains(remains)

                context = {'remains_contlog': df_remains,
                           'category': CategoryRemains.objects.all()}

                return render(request, template_name='remains/remains_contlog.html', context=context)

            else:
                remains = Remains.objects.filter(city=ajax['city_name'], status=ajax['code_category'])

        elif ajax['code_category'] == 'i2l':

            if ajax['city_name'] == 'kontinent':

                remains = pd.DataFrame(Remains.objects.filter(launch=ajax['code_category']).values())

                df_remains = contlog_remains(remains)

                context = {'remains_contlog': df_remains,
                           'category': CategoryRemains.objects.all()}

                return render(request, template_name='remains/remains_contlog.html', context=context)

            else:
                remains = Remains.objects.filter(city=ajax['city_name'], launch=ajax['code_category'])

        else:

            if ajax['city_name'] == 'kontinent':

                remains = pd.DataFrame(Remains.objects.filter(code_category=ajax['code_category']).values())

                df_remains = contlog_remains(remains)

                context = {'remains_contlog': df_remains,
                           'category': CategoryRemains.objects.all()}

                return render(request, template_name='remains/remains_contlog.html', context=context)

            else:

                remains = Remains.objects.filter(city=ajax['city_name'], code_category=ajax['code_category'])

        context = {'remains': remains,
                   'category': CategoryRemains.objects.all()}

        return render(request, template_name='remains/remains_table.html', context=context)

    else:
        context = {'title': 'Остатки'}
        return render(request, template_name='remains/index.html', context=context)
