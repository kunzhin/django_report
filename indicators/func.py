import pandas as pd
import numpy as np
from time import time
from io import BytesIO
import requests
import datetime
import time
from dateutil.relativedelta import relativedelta

from django.http import HttpResponse
from django.db.models import Sum, Q
from .models import IdeaToLaunch, Report07, TaskCategory, Report145, TopCategory, VolumeCategory, Report770
from .models import ClientException, DistrTaskPlan, I2lTaskPlan

from report_audit_control.date_work import work_day
from report_audit_control.env_var import BOT_TOKEN, CHANNEL_ID
from report_audit_control.date_work import MONTH_NUMBER, current_month, previous_month, NUMBER_MONTH, day_end_month
from report_audit_control.date_work import day_begin_month, previous_day_month


def send_telegram(text: str):
    requests.get('https://api.telegram.org/bot{}/sendMessage'.format(BOT_TOKEN), params=dict(chat_id=CHANNEL_ID, text=text))


# Функция применения классов Bootstrap для DataFrame
def df_to_html(df, table_id: str):
    return df.to_html(index=False,
                      table_id=table_id,
                      classes='table table-hover table-sm align-middle table-bordered'
                      ).replace("<thead>",
                                "<thead class='align-middle table-dark'>"
                                ).replace("<th>",
                                          "<th scope='col' class='text-center' style = 'width: 100px;'>"
                                          ).replace("<td>",
                                                    "<td class='text-center'>")


# Класс проверки наличия ключа, если отсутствует - возвращет свое значение
class DictMiss(dict):
    def __missing__(self, key):
        return key


# Словарь дубликатов ТопХ, нужно перенести в модель данных.
dbc_replace = {'DBC0000174': 'DBC0008875',
               'DBC0000175': 'DBC0008868',
               'DBC0008866': 'DBC0008868',
               'DBC0000180': 'DBC0008871',
               'DBC0008870': 'DBC0008871',
               'DBC0002537': 'DBC0008865',
               'DBC0007438': 'DBC0008872',
               'DBC0007439': 'DBC0008867',
               'DBC0008271': 'DBC0008873',
               'DBC0008885': 'DBC0000096',
               'DBC0006449': 'DBC0000082',
               }
'''
# Доп.дублирующие позиции ТопХ в Августе 2022г
dbc_replace.update({'DBC0007200': 'DBC0003346',
                    'DBC0003344': 'DBC0009014',
                    'DBC0003345': 'DBC0009020'
                    })
'''


class UserTask(object):
    def __init__(self, territory, user):
        self.user = user
        self.territory = territory

        self._task = DistrTaskPlan.objects.all().values_list('distr_task', flat=True).distinct()

        self._plan = pd.DataFrame(DistrTaskPlan.objects.filter(**{self.user: self.territory}
                                                               ).values('distr_task', 'target'))

        # -----------------Усиление кофе-------------
        start_time = time.time()
        self._coffee = pd.DataFrame(Report07.objects.filter(**{self.user: self.territory},
                                                            date_shipment__range=(
                                                                day_begin_month(previous_day_month(1)),
                                                                day_end_month()),
                                                            dbc_name__in=TaskCategory.objects.filter(
                                                                distr_task='home_shelf'
                                                            ).values_list('dbc_name'),
                                                            tier='Tier TT'
                                                            ).exclude(
            channel_tt='Wholesalers').values('code_tt', 'name_tt', 'address_tt'
                                             ).annotate(Coffee=Sum('sum_sell')
                                                        ).filter(Coffee__gt=3100))

        if self._coffee.empty:
            self._coffee = pd.DataFrame(columns=['code_tt', 'name_tt', 'address_tt', 'Coffee'])

        print(f"--- {round(time.time() - start_time, 6)} seconds формируем усиление Кофе ---")

        # ----------------Усиление магги-------------
        start_time = time.time()
        self._maggi = pd.DataFrame(Report145.objects.filter(**{self.user: self.territory,
                                                               'category': '110 Кулинария',
                                                               'month': current_month()},
                                                            tier='Tier TT'
                                                            ).exclude(channel_tt='Wholesalers'
                                                                      ).values('code_tt', 'name_tt', 'address_tt'
                                                                               ).annotate(
            Maggi=Sum('sum_sell')
        ).filter(Maggi__gt=900))

        if self._maggi.empty:
            self._maggi = pd.DataFrame(columns=['code_tt', 'name_tt', 'address_tt', 'Maggi'])

        print(f"--- {round(time.time() - start_time, 6)} seconds формируем усиление Магги ---")

        # ----------------Усиление пурина------------
        start_time = time.time()
        self._purina = pd.DataFrame(Report145.objects.filter(**{self.user: self.territory,
                                                                'category__in': (
                                                                    '170 Сухие корма для кошек',
                                                                    '172 Влажные корма для кошек',
                                                                    '176 Влажные корма для собак'),
                                                                'month': current_month()},
                                                             purina_except__isnull=True,
                                                             tier='Tier TT'
                                                             ).exclude(
            channel_tt='Wholesalers'
        ).values('code_tt', 'name_tt', 'address_tt'
                 ).annotate(Purina=Sum('sum_sell')
                            ).filter(Purina__gt=600))

        if self._purina.empty:
            self._purina = pd.DataFrame(columns=['code_tt', 'name_tt', 'address_tt', 'Purina'])

        print(f"--- {round(time.time() - start_time, 6)} seconds формируем усиление Пурина ---")

        # -----------------Усиление Какао 13.5г-------------
        start_time = time.time()
        self._cocoa = pd.DataFrame(Report07.objects.filter(**{self.user: self.territory},
                                                           date_shipment__range=(
                                                               day_begin_month(),
                                                               day_end_month()),
                                                           dbc_name__in=TaskCategory.objects.filter(
                                                               **{'distr_task': 'cacao13,5g'}
                                                           ).values_list('dbc_name'),
                                                           tier='Tier TT'
                                                           ).exclude(
            channel_tt='Wholesalers').values('code_tt', 'name_tt', 'address_tt'
                                             ).annotate(Cocoa=Sum('count_piece')
                                                        ).filter(Cocoa__gt=15))

        if self._cocoa.empty:
            self._cocoa = pd.DataFrame(columns=['code_tt', 'name_tt', 'address_tt', 'Cocoa'])

        print(f"--- {round(time.time() - start_time, 6)} seconds формируем усиление Какао ---")

        # -----------------Фотопоток-----------------
        self._foto = pd.DataFrame(
            Report770.objects.filter(Q(category='Усиление Кофе', month__in=[current_month(), previous_month()]) |
                                     Q(category='Усиление Магги', month=current_month()) |
                                     Q(category='Усиление Пурина', month=current_month()),
                                     **{self.user: self.territory},
                                     status=1).values('code_tt', 'category')
        ).replace(
            {'Усиление Кофе': 'Coffee', 'Усиление Магги': 'Maggi', 'Усиление Пурина': 'Purina'})
        if self._foto.empty:
            self._foto = pd.DataFrame(columns=['code_tt', 'category'])

        self._fact = pd.concat([self._coffee, self._maggi, self._purina, self._cocoa], ignore_index=True
                               ).set_index(['code_tt', 'name_tt', 'address_tt']).stack().reset_index(
        ).merge(self._foto, left_on=['code_tt', 'level_3'], right_on=['code_tt', 'category'], how='left'
                ).rename({'level_3': 'distr_task', 'category': 'Фото', 0: 'fact'}, axis=1).drop_duplicates()

    def foto_nan(self, task):
        result = self._fact.loc[(self._fact['distr_task'] == task) & self._fact['Фото'].isnull()]

        return result[['name_tt', 'address_tt']].rename({'name_tt': 'Наименование ТТ',
                                                         'address_tt': 'Адрес ТТ'}, axis=1)

    def result(self):
        if not self._plan.empty:
            self._plan = self._plan.groupby(['distr_task']).sum(numeric_only=True).reset_index()
        else:
            self._plan = pd.DataFrame.from_dict({i: 0 for i in self._task},
                                                orient='index', columns=['target']
                                                ).reset_index().rename({'index': 'distr_task'}, axis=1)

        result = pd.pivot_table(self._fact, values=['fact', 'Фото'], index=['distr_task'],
                                aggfunc={'fact': 'count', 'Фото': 'count'}).reset_index()

        if result.empty:
            result = pd.DataFrame({'distr_task': ['Coffee', 'Maggi', 'Purina', 'Cocoa'],
                                   'fact': [0, 0, 0],
                                   'Фото': [0, 0, 0]}
                                  )

        result = self._plan.merge(result, on='distr_task', how='left').fillna(0)

        result['%'] = round((result['fact'] / result['target']) * 100, 0).replace(np.nan, 0).replace(np.inf, 100)

        result['%'] = result['%'].apply(lambda x: '{0:.0f}%'.format(x))

        result['Осталось'] = result['target'] - result['fact']

        result['План на день'] = round(result['Осталось'] / work_day(), 0)

        result['% Фото'] = round((result['Фото'] / result['fact']) * 100, 0).replace(np.nan, 0).replace(np.inf, 100)

        result['% Фото'] = result['% Фото'].apply(lambda x: '{0:.0f}%'.format(x))

        return result.rename({'distr_task': 'Задача',
                              'target': 'План',
                              'fact': 'Факт'}, axis=1
                             ).replace({'Coffee': 'Усиление Кофе',
                                        'Cocoa': 'Хрутка 13.5г',
                                        'Maggi': 'Усиление Магги',
                                        'Purina': 'Усиление Пурина'})[
            ['Задача', 'План', 'Факт', '%', 'Осталось', 'Фото', '% Фото', 'План на день']]

    def launches(self):
        # Запуски
        total = time.time()
        launches = IdeaToLaunch.objects.all().values_list('task_name', flat=True)

        result = pd.DataFrame()

        for task in launches:
            plan = pd.DataFrame(I2lTaskPlan.objects.filter(**{self.user: self.territory},
                                                           distr_task=task).values('view_task', 'target')).fillna(0)

            if plan.empty:
                plan = pd.DataFrame({'view_task': ['DISTR', 'VOL'], 'target': [0, 0]})

            plan = pd.pivot_table(plan,
                                  columns='view_task',
                                  values='target',
                                  aggfunc='sum').rename(index={'target': task}
                                                        ).reset_index().rename({'index': 'task'}, axis=1)

            plan.columns.names = [None]

            dbc = IdeaToLaunch.objects.filter(task_name=task).values_list('dbc__DBC_name', flat=True)

            min_threshold = IdeaToLaunch.objects.filter(task_name=task).values_list('min_threshold', flat=True)

            launch_day_start = IdeaToLaunch.objects.filter(task_name=task).values_list('day_start', flat=True)[0]
            launch_day_end = IdeaToLaunch.objects.filter(task_name=task).values_list('day_end', flat=True)[0]

            # print(f'Month_start: {launch_day_start}, Month_end: {launch_day_end}')

            tier = IdeaToLaunch.objects.filter(task_name=task).values_list('tier__tier', flat=True)

            channel = IdeaToLaunch.objects.filter(task_name=task).values_list('channel__channel', flat=True)

            func_launch = IdeaToLaunch.objects.filter(task_name=task).values_list('func_launch', flat=True)

            start_time = time.time()
            data = pd.DataFrame(Report07.objects.filter(**{self.user: self.territory},
                                                        dbc_name__in=dbc,
                                                        date_shipment__range=(launch_day_start, launch_day_end),
                                                        tier__in=tier,
                                                        channel_tt__in=channel,
                                                        ).values('code_tt', 'dbc_name', 'count_piece', 'sum_sell'))
            if data.empty:
                data = pd.DataFrame({'code_tt': [0], 'dbc_name': [0], 'count_piece': [0], 'sum_sell': [0]})

            print(f"--- {round(time.time() - start_time, 6)} seconds Сформированы данные по запуску {task} ---")

            if func_launch[0] == 'sum_dbc':
                # Расчет зачета по сумме проданных SKU в ТТ
                print('Расчет по сумме проданного кол-ва всех SKU в ТТ по порогу | sum_dbc')
                # Группируем по коду ТТ кол-во и сумму
                data = data.groupby('code_tt').sum(['count_piece', 'sum_sell']).reset_index()
                # Определяем какие ТТ проходят в зачет по порогу зачета задачи
                data['threshold'] = np.where(data['count_piece'] >= min_threshold[0], 1, 0)
                # Добавляем наименование задачи
                data['task'] = task
                # Группируем по наименованию задачи кол-во сработанных ТТ и сумму продаж в объеме, убираем сумму общего кол-ва
                data = data.groupby('task').sum(['threshold', 'sum_sell']).reset_index().drop('count_piece', axis=1)

                data = data.merge(plan, on='task', how='left')

                result = pd.concat([result, data])

            elif func_launch[0] == 'count_dbc':
                print('Расчет общего кол-ва проданных DBC по порогу | count_dbc')
                data = data.groupby(['code_tt', 'dbc_name']).sum(['count_piece', 'sum_sell']).reset_index()
                data['threshold'] = np.where(data['count_piece'] >= min_threshold[0], 1, 0)
                data['task'] = task
                data = data.groupby('task').sum(['threshold', 'sum_sell']).reset_index().drop('count_piece', axis=1)

                data = data.merge(plan, on='task', how='left')

                result = pd.concat([result, data])

            elif func_launch[0] == 'count_sum_dbc':
                print('Расчет порога для каждого DBC для зачета 1тт | count_sum_dbc')
                data = data.groupby(['code_tt', 'dbc_name']).sum(['count_piece', 'sum_sell']).reset_index()
                data['threshold'] = np.where(data['count_piece'] >= min_threshold[0], 1, 0)
                data = data.groupby('code_tt').sum(['threshold', 'sum_sell']).reset_index().drop('count_piece', axis=1)
                data['threshold'] = np.where(data['threshold'] >= len(dbc), 1, 0)
                data['task'] = task
                data = data.groupby('task').sum(['threshold', 'sum_sell']).reset_index()

                data = data.merge(plan, on='task', how='left')

                result = pd.concat([result, data])

        result['Покрытие %'] = round((result['threshold'] / result['DISTR']) * 100, 0
                                     ).replace(np.nan, 0
                                               ).replace(np.inf, 100).apply(lambda x: '{0:.0f}%'.format(x))

        result['Объем %'] = round((result['sum_sell'] / result['VOL']) * 100, 0
                                  ).replace(np.nan, 0
                                            ).replace(np.inf, 100).apply(lambda x: '{0:.0f}%'.format(x))

        result['План на день'] = round((result['DISTR'] - result['threshold']) / work_day(), 0)

        result = result.rename({'task': 'Задача',
                                'sum_sell': 'Факт Объем',
                                'threshold': 'Факт Покрытие',
                                'DISTR': 'План Покрытие',
                                'VOL': 'План Объем'}, axis=1)

        result = result[['Задача',
                         'План Покрытие',
                         'Факт Покрытие',
                         'Покрытие %',
                         'План Объем',
                         'Факт Объем',
                         'Объем %',
                         'План на день']]

        print(f"--- {round(time.time() - total, 6)} seconds Сформированы все данные!!! ---")

        return result


class HistoryTT(object):

    def __init__(self, user, territory, name_tt, address):
        # Получаем должность user -> DSM, TSM, ESR
        self.user = user
        # Получаем территорю user
        self.territory = territory
        # Получаем имя тт
        self.name_tt = name_tt
        # Получаем адрес тт
        self.address = address
        # Устанавливаем период получания данных
        self._period_data = 6
        # Получаем первое число месяца _period_data месяцев назад
        self._month_start = day_begin_month(datetime.datetime.today() - relativedelta(months=self._period_data))
        # Получаем последний день текущего месяца от сегодняшнего дня
        self._month_end = day_end_month(datetime.datetime.today())

        # Получаем категории усилений
        start_time = time.time()
        self._cat_strength = pd.DataFrame(TaskCategory.objects.all().values('dbc_name', 'distr_task'))
        print(f"--- {round(time.time() - start_time, 6)} seconds Получаем категории усилений ---")

        # Получаем данные по фотопотоку
        start_time = time.time()
        self._fotostream = pd.DataFrame(Report770.objects.filter(**{self.user: self.territory,
                                                                    'name_tt': self.name_tt,
                                                                    'address_tt': self.address}).values())
        print(f"--- {round(time.time() - start_time, 6)} seconds Получаем данные по фотопотоку ---")

        # Получаем продажи по Усилению Магги из 145го отчета за текущий месяц
        start_time = time.time()
        data_maggi = Report145.objects.filter(**{self.user: self.territory,
                                                 'name_tt': self.name_tt,
                                                 'address_tt': self.address,
                                                 'category': '110 Кулинария',
                                                 'month': current_month()}
                                              ).exclude(channel_tt='Wholesalers'
                                                        ).values('code_tt', 'month', 'category',
                                                                 'dbc',
                                                                 'sum_sell')
        print(
            f"--- {round(time.time() - start_time, 6)} seconds Получаем продажи по Усилению Магги из 145го отчета за текущий месяц ---")
        start_time = time.time()
        self._strength_maggi = pd.DataFrame(data_maggi)
        print(f"--- {round(time.time() - start_time, 6)} seconds Получаем продажи по Усилению Магги_DF ---")

        # Получаем продажи по Усилению Пурина из 145го отчета за текущий месяц
        start_time = time.time()
        self._strength_purina = pd.DataFrame(Report145.objects.filter(**{self.user: self.territory,
                                                                         'name_tt': self.name_tt,
                                                                         'address_tt': self.address,
                                                                         'category__in': ('170 Сухие корма для кошек',
                                                                                          '172 Влажные корма для кошек',
                                                                                          '176 Влажные корма для собак'),
                                                                         'month': current_month()}
                                                                      ).exclude(channel_tt='Wholesalers'
                                                                                ).values('code_tt', 'month', 'category',
                                                                                         'dbc',
                                                                                         'sum_sell'))
        print(
            f"--- {round(time.time() - start_time, 6)} seconds Получаем продажи по Усилению Пурина из 145го отчета за текущий месяц ---")

        # Получаем продажи общие за период
        start_time = time.time()
        self._data = pd.DataFrame(Report07.objects.filter(**{self.user: self.territory,
                                                             'name_tt': self.name_tt,
                                                             'address_tt': self.address},
                                                          date_shipment__range=(self._month_start, self._month_end)
                                                          ).values())
        print(f"--- {round(time.time() - start_time, 6)} seconds Получаем продажи общие за период ---")

        # start_time = time.time()
        # self._data = pd.DataFrame(data_07)
        # print(f"--- {round(time.time() - start_time, 6)} seconds DF общие за период ---")

    # Возвращаем канал ТТ
    def channel(self):
        return self._data['channel_tt'].iloc[0]

    # Возвращаем последнюю дату доставки в тт
    def last_date_shipment(self):
        return self._data['date_shipment'].max()

    # Возвращаем сеть ТТ(вывеску)
    def network(self):
        return self._data['network'].iloc[0]

    # Возвращаем среднее кол-во заказов в месяц
    def avg_num_orders(self):
        return round(len(self._data['date_shipment'].unique()) / self._period_data, 2)

    # Возвращаем DataFrame с продажами ТопХ позиций за период
    def topx(self):
        try:
            if not self._data.empty:

                topx_fact = self._data[['dbc', 'count_piece', 'month']]

                topx_fact = pd.pivot_table(topx_fact,
                                           index=['dbc'],
                                           columns='month',
                                           values='count_piece',
                                           aggfunc='sum').reset_index()

                cat_topx = pd.DataFrame(TopCategory.objects.all().values('rev_group_top', 'dbc', 'dbc_name'))

                topx_fact['dbc'] = topx_fact['dbc'].map(DictMiss(dbc_replace))

                cat_topx['dbc'] = cat_topx['dbc'].map(DictMiss(dbc_replace))

                cat_topx = cat_topx.drop_duplicates(subset='dbc')

                topx_fact = cat_topx.merge(topx_fact, left_on='dbc', right_on='dbc', how='left'
                                           ).dropna(subset=['dbc_name']
                                                    ).drop('dbc_name', axis=1)

                topx_fact['dbc'] = topx_fact['dbc'].map(DictMiss(cat_topx.set_index('dbc')['dbc_name']))

                df_fact = pd.DataFrame()

                for category in topx_fact['rev_group_top'].drop_duplicates():
                    df1 = topx_fact.loc[topx_fact['rev_group_top'].isin([category])].groupby(['rev_group_top']).count()

                    df2 = topx_fact.loc[topx_fact['rev_group_top'].isin([category])].groupby(['dbc']).sum(numeric_only=True)

                    df_fact = pd.concat([df_fact, df1, df2])

                df_fact = df_fact.drop('dbc', axis=1
                                       ).rename(columns=lambda col: NUMBER_MONTH[col]
                                                ).reset_index().rename({'index': 'ТОП Х'}, axis=1
                                                                       )

                rev_group_top = ['COFFEE', 'CONFECTIONERY', 'CPW', 'CULINARY', 'Nesquik', 'PURINA']

                # Добавляем ТОТАЛ по всем категориям
                df_fact = pd.concat([df_fact, df_fact.loc[
                    df_fact['ТОП Х'].isin(rev_group_top)].sum(numeric_only=True
                                                              ).rename('Total'
                                                                       ).to_frame().T]).fillna('').replace({0: ''})

                return df_fact
        except KeyError:

            df_res = pd.DataFrame()

            return df_res

    # Возвращаем DataFrame с продажами по объему за период
    def volume(self):
        try:
            if not self._data.empty:
                volume = self._data[['group', 'sum_sell', 'month']]
                volume_category = pd.DataFrame(VolumeCategory.objects.all().values())

                volume = pd.pivot_table(volume,
                                        index='group',
                                        columns='month',
                                        values='sum_sell',
                                        aggfunc='sum').reset_index()

                volume = volume_category.merge(volume, left_on='group', right_on='group', how='left'
                                               ).drop(['id', 'group'], axis=1)

                df_fact_total = pd.DataFrame()

                for category in volume['rev_group'].drop_duplicates():
                    df1 = volume.loc[volume['rev_group'].isin([category])].groupby(
                        ['rev_group']).sum(numeric_only=True)

                    df2 = volume.loc[volume['rev_group'].isin([category])].groupby(
                        ['rev_pre_group']).sum(numeric_only=True)

                    df_fact_total = pd.concat([df_fact_total, df1, df2])

                df_fact_total = df_fact_total.rename(columns=lambda col: NUMBER_MONTH[col]
                                                     ).reset_index().rename({'index': 'ОБЪЕМ'}, axis=1)

                rev_group_vol = ['COFFEE', 'Food&Diary', 'CPW', 'CONFECTIONERY', 'PURINA']

                # Добавляем ТОТАЛ по всем категориям
                df_fact_total = pd.concat([df_fact_total,
                                           df_fact_total.loc[df_fact_total['ОБЪЕМ'].isin(rev_group_vol)].sum(
                                               numeric_only=True).rename('Total'
                                                                         ).to_frame().T]).fillna(
                    '').replace({0: ''})

                return df_fact_total

        except KeyError:

            df_fact_total = pd.DataFrame()

            return df_fact_total

    # Возвращаем статус по усилению Кофе или сумму догрузки
    def coffee_strength(self):
        # Усиление Кофе
        try:
            if not self._data.empty:
                month = [MONTH_NUMBER[previous_month()], MONTH_NUMBER[current_month()]]
                coffee_strength = self._data.loc[self._data['month'].isin(month)]

                coffee_strength = coffee_strength.merge(self._cat_strength, on='dbc_name', how='left')

                coffee_strength = coffee_strength.loc[
                    (coffee_strength['distr_task'] == 'home_shelf') & (coffee_strength['channel_tt'] != 'Wholesalers')]

                coffee_strength = pd.pivot_table(coffee_strength, values='sum_sell',
                                                 index='code_tt',
                                                 columns='distr_task',
                                                 aggfunc=np.sum)

                coffee_strength['home_shelf'] = np.where(coffee_strength['home_shelf'] >= 3100,
                                                         'Зачёт',
                                                         round(3100 - coffee_strength['home_shelf'], 2))

                return coffee_strength['home_shelf'].values[0]

            else:
                return 3100

        except (KeyError, UnboundLocalError):
            return 3100

    # Возвращаем статус по усилению Магги или сумму догрузки
    def maggi_strenght(self):
        try:
            if not self._strength_maggi.empty:

                str_maggi = pd.pivot_table(self._strength_maggi,
                                           values='sum_sell',
                                           index='code_tt',
                                           columns='category',
                                           aggfunc=np.sum)
                str_maggi['110 Кулинария'] = np.where(str_maggi['110 Кулинария'] >= 900,
                                                      'Зачёт',
                                                      round(900 - str_maggi['110 Кулинария'], 2))
                return str_maggi['110 Кулинария'].values[0]

            else:
                return 900

        except (KeyError, UnboundLocalError):
            return 900

    # Возвращаем статус по усилению Пурина или сумму догрузки
    def purina_strenght(self):
        if ClientException.objects.filter(
                code_tt=self._data['code_tt'].drop_duplicates().values[0]).exists():
            return 'Исключение'
        else:
            try:
                if not self._strength_purina.empty:
                    str_purina = pd.pivot_table(self._strength_purina,
                                                values='sum_sell',
                                                index='code_tt',
                                                columns='dbc',
                                                aggfunc=np.sum)

                    str_purina['count'] = str_purina.count(axis=1)
                    str_purina['sum'] = str_purina.sum(axis=1)

                    str_purina['Усиление Пурина'] = np.where((str_purina['sum'] >= 600) & (str_purina['count'] >= 1),
                                                             'Зачёт', str(round(600 - str_purina['sum'].values[0], 2)) +
                                                             ' и ' + str(1 - str_purina['count'].values[0]) + ' sku')

                    return str_purina['Усиление Пурина'].values[0]

                else:
                    return 600

            except (KeyError, UnboundLocalError):
                return 600

    # Возвращаем статус по наличию фотографии Усилений в 770м отчете, дату последнего фото из ТТ
    def fotostream(self):
        if not self._fotostream.empty:
            coffee = self._fotostream.loc[(self._fotostream['category'] == 'Усиление Кофе') &
                                          (self._fotostream['status'] == 1)]

            maggi = self._fotostream.loc[(self._fotostream['category'] == 'Усиление Магги') &
                                         (self._fotostream['status'] == 1) &
                                         (self._fotostream['month'] == current_month())]

            purina = self._fotostream.loc[(self._fotostream['category'] == 'Усиление Пурина') &
                                          (self._fotostream['status'] == 1) &
                                          (self._fotostream['month'] == current_month())]

            if coffee.empty:
                coffee = 'Нет фото'
            else:
                coffee = coffee['date_foto'].max()

            if maggi.empty:
                maggi = 'Нет фото'
            else:
                maggi = maggi['date_foto'].max()

            if purina.empty:
                purina = 'Нет фото'
            else:
                purina = purina['date_foto'].max()

            return [coffee, maggi, purina]

        else:
            return ['Нет фото'] * 3


def get_excel_file(df, filename: str, index: bool = False):
    response = BytesIO()
    writer = pd.ExcelWriter(response, engine='xlsxwriter', engine_kwargs={'options': {'strings_to_formulas': False}})
    df.to_excel(writer, sheet_name='Report', index=index)
    writer.close()
    response.seek(0)

    response = HttpResponse(response.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=%s" % filename

    return response


# Функция подсчета значений в столбце Dataframe
def count_tt(df, col, value):
    try:
        if value == 'Зачёт':  # Считаем кол-во точек которые попали в зачёт
            df = df[col].loc[(df[col] == 'Зачёт')]
            counts_tt = df.count()

        else:  #
            df = df[col].loc[(df[col] != 'Зачёт') & (df[col] != '')].astype(float)

            if value != 0:  # Считаем кол-во точек на догрузку от указанного порога value
                counts_tt = df.loc[df <= value].count()

            else:  # Если value = 0 считаем все значения
                counts_tt = df.count()
    except KeyError:
        counts_tt = 0

    return counts_tt


def tt_info(tt_list, value, param_user, xlsx=False):
    month_end = MONTH_NUMBER[current_month()]

    try:
        start_time = time.time()
        fact_two_month = pd.DataFrame(
            Report07.objects.filter(**{param_user: value}, date_shipment__range=(
                day_begin_month(previous_day_month(1)),
                day_end_month())
                                    ).values('code_tt', 'code_tt_kis', 'channel_tt', 'tier', 'month', 'dbc_name',
                                             'topx',
                                             'sum_sell'))
        print(f"--- {round(time.time() - start_time, 6)}  seconds Прочитали факт за 2 месяца ---")

        start_time = time.time()
        cat_strength = pd.DataFrame(TaskCategory.objects.all().values('dbc_name', 'distr_task'))
        print(f"--- {round(time.time() - start_time, 6)}  seconds Прочитали DBC по Усилениям ---")

        fact_two_month = fact_two_month.merge(cat_strength, on='dbc_name', how='left')

        start_time = time.time()
        strength = pd.DataFrame(Report145.objects.filter(**{param_user: value},
                                                         tier='Tier TT'
                                                         ).exclude(channel_tt='Wholesalers'
                                                                   ).values('code_tt', 'month', 'category', 'dbc',
                                                                            'sum_sell'))
        print(f"--- {round(time.time() - start_time, 6)}  seconds Прочитали 145й отчет ---")


    except (KeyError, UnboundLocalError):
        pass

    # Читаем исключения по Пурине
    start_time = time.time()
    client_except = pd.DataFrame(ClientException.objects.all().values('code_tt', 'status'))
    print(f"--- {round(time.time() - start_time, 6)}  seconds Прочитали исключения по Пурине ---")

    # Читаем данные фотопотока
    start_time = time.time()
    report_770 = pd.DataFrame(
        Report770.objects.filter(Q(category='Усиление Кофе', month__in=[current_month(), previous_month()]) |
                                 Q(category='Усиление Магги', month=current_month()) |
                                 Q(category='Усиление Пурина', month=current_month()),
                                 **{param_user: value},
                                 status=1
                                 ).values('code_tt', 'category'))

    print(f"--- {round(time.time() - start_time, 6)}  seconds Прочитали 770й отчет по фото ---")

    # Продажи текущего месяца, sell - объем, top - топх
    try:
        start_time = time.time()
        fact_month = fact_two_month.loc[fact_two_month['month'] == month_end]

        fact_month_sell = fact_month[['code_tt', 'sum_sell']].groupby('code_tt').sum(numeric_only=True).round({'sum_sell': 2})

        # fact_month_top = fact_month[['code_tt', 'topx']
        # ].loc[(fact_month['topx'] == 'ok') & (fact_month['channel_tt'] != 'Wholesalers')
        #       ].groupby('code_tt').count()
        #
        # tt_list = tt_list.merge(fact_month_top, left_on='code_tt', right_on='code_tt', how='left')

    except (KeyError, UnboundLocalError):
        fact_month_sell = pd.DataFrame({'sum_sell': [], 'code_tt': []})

    tt_list = tt_list.merge(fact_month_sell, left_on='code_tt', right_on='code_tt', how='left').drop_duplicates()
    print(f"--- {round(time.time() - start_time, 6)}  seconds Сформированы продажи текущего месяца Объем ---")

    # Усиление Кофе
    try:
        start_time = time.time()
        coffee_strength = fact_two_month.loc[
            (fact_two_month['distr_task'] == 'home_shelf') &
            (fact_two_month['channel_tt'] != 'Wholesalers') &
            (fact_two_month['tier'] == 'Tier TT')]

        coffee_strength = pd.pivot_table(coffee_strength, values='sum_sell',
                                         index='code_tt',
                                         columns='distr_task',
                                         aggfunc=np.sum)

        coffee_strength['home_shelf'] = np.where(coffee_strength['home_shelf'] >= 3100,
                                                 'Зачёт',
                                                 round(3100 - coffee_strength['home_shelf'], 2))
    except (KeyError, UnboundLocalError):
        coffee_strength = pd.DataFrame({'home_shelf': [], 'code_tt': []})

    tt_list = tt_list.merge(coffee_strength, left_on='code_tt', right_on='code_tt', how='left').drop_duplicates()
    print(f"--- {round(time.time() - start_time, 6)}  seconds Сформирован Усиление Кофе ---")

    # Усиление Магги
    try:
        start_time = time.time()
        str_maggi = strength.loc[(strength['month'] == current_month()) & (strength['category'] == '110 Кулинария')]
        str_maggi = pd.pivot_table(str_maggi,
                                   values='sum_sell',
                                   index='code_tt',
                                   columns='category',
                                   aggfunc=np.sum)
        str_maggi['110 Кулинария'] = np.where(str_maggi['110 Кулинария'] >= 900,
                                              'Зачёт',
                                              round(900 - str_maggi['110 Кулинария'], 2))

    except (KeyError, UnboundLocalError):
        str_maggi = pd.DataFrame({'110 Кулинария': [], 'code_tt': []})

    tt_list = tt_list.merge(str_maggi, left_on='code_tt', right_on='code_tt', how='left').drop_duplicates()
    print(f"--- {round(time.time() - start_time, 6)}  seconds Сформирован Усиление Магги ---")

    # Усиление Пурина
    try:
        start_time = time.time()

        period = [current_month()]
        category = ['170 Сухие корма для кошек', '172 Влажные корма для кошек', '176 Влажные корма для собак']
        str_purina = strength.loc[(strength['month'].isin(period)) & (strength['category'].isin(category))]

        str_purina = pd.pivot_table(str_purina,
                                    values='sum_sell',
                                    index='code_tt',
                                    columns='dbc',
                                    aggfunc=np.sum)

        str_purina['count'] = str_purina.count(axis=1)
        str_purina['sum'] = str_purina.sum(axis=1)

        str_purina['Усиление Пурина'] = np.where((str_purina['sum'] >= 600) & (str_purina['count'] >= 1),
                                                 'Зачёт', round(600 - str_purina['sum'], 2))

        str_purina = str_purina[['Усиление Пурина']]

    except (KeyError, UnboundLocalError):
        str_purina = pd.DataFrame({'Усиление Пурина': [], 'code_tt': []})

    tt_list = tt_list.merge(str_purina, left_on='code_tt', right_on='code_tt', how='left')

    tt_list = tt_list.merge(client_except, on='code_tt', how='left')

    tt_list['Усиление Пурина'] = np.where(tt_list['status'] != 'Исключение',
                                          tt_list['Усиление Пурина'],
                                          tt_list['status'])
    tt_list = tt_list.drop('status', axis=1).drop_duplicates()
    print(f"--- {round(time.time() - start_time, 6)}  seconds Сформирован Усиление Пурина ---")


    # Фотопоток
    try:
        start_time = time.time()
        report_770 = report_770.drop_duplicates(subset=['code_tt', 'category'], keep='last')
        foto_pivot = pd.pivot_table(report_770, index=['code_tt'], values='category',
                                    aggfunc=lambda x: " ".join(sorted(x + ''))
                                    ).rename({'category': 'Фото'}, axis=1)

        tt_list = tt_list.merge(foto_pivot, on='code_tt', how='left').drop_duplicates()
        print(f"--- {round(time.time() - start_time, 6)}  seconds Подтянуты данные по фотопотоку ---")

    except (KeyError, UnboundLocalError):
        pass

    launches = IdeaToLaunch.objects.filter(info_tt_view=True).values_list('dbc__DBC_name', flat=True)

    for dbc in launches:
        launch_day_start = IdeaToLaunch.objects.filter(dbc__DBC_name=dbc).values_list('day_start', flat=True)[0]
        launch_day_end = IdeaToLaunch.objects.filter(dbc__DBC_name=dbc).values_list('day_end', flat=True)[0]

        try:
            start_time = time.time()
            res = pd.DataFrame(Report07.objects.filter(dbc_name=dbc,
                                                       **{param_user: value},
                                                       date_shipment__range=(launch_day_start, launch_day_end)
                                                       ).values('dbc_name', 'code_tt_kis', 'count_piece'))

            res = pd.pivot_table(res, values='count_piece', index=['code_tt_kis'], columns='dbc_name', aggfunc=np.sum)
            # Добавление кол-ва сработавших ТТ по запуску
            # res = res.rename({res.columns[0]: res.columns[0] + ' (' + str(count_tt(res, res.columns[0], 0)) + ')'},
            #                  axis=1)

            tt_list = tt_list.merge(res, left_on='kis_code', right_on='code_tt_kis', how='left').drop_duplicates()
            print(f"--- {round(time.time() - start_time, 6)} seconds Подтянуты данные по запуску {dbc} ---")



        except KeyError:
            pass

    if not xlsx:
        # Сводный DataFrame
        tt_list = tt_list.drop(['code_tt', 'kis_code'], axis=1
                               ).rename({'address': 'Адрес',
                                         'tt_id__tt': 'Наименование ТТ',
                                         'day_route': 'День посещения',
                                         'topx': 'TOPX',
                                         'sum_sell': 'Продажи ' + current_month() + ' (' + str(
                                             count_tt(tt_list, 'sum_sell', 1500)) + ')',
                                         'home_shelf': 'Усиление Кофе (' + str(
                                             count_tt(tt_list, 'home_shelf', 1000)) + ')',
                                         '110 Кулинария': 'Усиление Магги (' + str(
                                             count_tt(tt_list, '110 Кулинария', 300)) + ')',
                                         'Усиление Пурина': 'Усиление Пурина (' + str(
                                             count_tt(tt_list, 'Усиление Пурина', 'Зачёт')) + ')',
                                         'cacao13,5g': 'Какао 13,5г (' + str(count_tt(tt_list, 'cacao13,5g', 0)) + ')'},
                                        axis=1
                                        ).fillna('')
    else:
        # Сводный DataFrame
        tt_list = tt_list.rename({'address': 'Адрес',
                                  'tt_id__esr_id__tsm_id__dsm_id__dsm': 'DSM',
                                  'tt_id__esr_id__tsm_id__tsm': 'TSM',
                                  'tt_id__esr_id__esr': 'ESR',
                                  'tier': 'Tier',
                                  'channel_tt': 'Канал ТТ',
                                  'code_tt': 'Код ТТ',
                                  'kis_code': 'КИС Код',
                                  'tt_id__tt': 'Наименование ТТ',
                                  'day_route': 'День посещения',
                                  'topx': 'TOPX',
                                  'sum_sell': 'Продажи ' + current_month() + ' (' + str(
                                      count_tt(tt_list, 'sum_sell', 1500)) + ')',
                                  'home_shelf': 'Усиление Кофе (' + str(
                                      count_tt(tt_list, 'home_shelf', 1000)) + ')',
                                  '110 Кулинария': 'Усиление Магги (' + str(
                                      count_tt(tt_list, '110 Кулинария', 300)) + ')',
                                  'Усиление Пурина': 'Усиление Пурина (' + str(
                                      count_tt(tt_list, 'Усиление Пурина', 'Зачёт')) + ')',
                                  'cacao13,5g': 'Какао 13,5г (' + str(count_tt(tt_list, 'cacao13,5g', 0)) + ')'},
                                 axis=1
                                 ).fillna('')

    return tt_list


# Функция формирования DataFrame по объему
def df_plan_tsm(volume_plan_tsm, volume_fact):
    df_list = []

    if not volume_plan_tsm.empty:

        for tier in volume_plan_tsm['tier'].drop_duplicates():

            df_plan = pd.DataFrame()

            for category in volume_plan_tsm['rev_group'].drop_duplicates():
                df1 = volume_plan_tsm.loc[
                    (volume_plan_tsm['rev_group'].isin([category])) & (volume_plan_tsm['tier'].isin([tier]))].groupby(
                    ['tier', 'rev_group']).sum(numeric_only=True)

                df2 = volume_plan_tsm[
                    volume_plan_tsm['rev_group'].isin([category]) & (volume_plan_tsm['tier'].isin([tier]))].groupby(
                    ['tier', 'rev_pre_group']).sum(numeric_only=True)

                df_plan = pd.concat([df_plan, df1, df2])

            if not volume_fact.empty:

                df_fact = pd.DataFrame()

                for category in volume_fact['rev_group'].drop_duplicates():
                    df1 = volume_fact.loc[
                        (volume_fact['rev_group'].isin([category])) & (volume_fact['tier'].isin([tier]))].groupby(
                        ['tier', 'rev_group']).sum(numeric_only=True)

                    df2 = volume_fact.loc[
                        (volume_fact['rev_group'].isin([category])) & (volume_fact['tier'].isin([tier]))].groupby(
                        ['tier', 'rev_pre_group']).sum(numeric_only=True)

                    df_fact = pd.concat([df_fact, df1, df2])

                df_res = df_plan.merge(df_fact,
                                       left_on=['tier', 'rev_group'],
                                       right_on=['tier', 'rev_group'],
                                       how='left').fillna(0).reset_index()
            else:
                df_fact = pd.DataFrame(columns=['tier', 'rev_group', 'sum_sell'])

                df_res = df_plan.merge(df_fact,
                                       left_on=['tier', 'rev_group'],
                                       right_on=['tier', 'rev_group'],
                                       how='left').fillna(0)

            df_res = pd.concat([df_res,
                                df_res.loc[df_res['rev_group'].isin(['COFFEE',
                                                                     'Food&Diary',
                                                                     'CPW',
                                                                     'CONFECTIONERY',
                                                                     'PURINA'])].sum(numeric_only=True
                                                                                     ).rename('Total'
                                                                                              ).to_frame().T]).fillna(
                '')

            df_res['%'] = round((df_res['sum_sell'] / df_res['target']) * 100, 0
                                ).replace(np.nan, 0
                                          ).replace(np.inf, 100)

            df_res['%'] = df_res['%'].apply(lambda x: '{0:.0f}%'.format(x))

            df_res['Осталось'] = df_res['target'] - df_res['sum_sell']

            df_res['План на день'] = round(df_res['Осталось'] / work_day(), 2)

            df_list.append(df_res.rename({'tier': 'Tier',
                                          'rev_group': 'Revision Group',
                                          'target': 'План',
                                          'sum_sell': 'Факт'}, axis=1).drop('id', axis=1))

        df_plan_total = pd.DataFrame()

        for category in volume_plan_tsm['rev_group'].drop_duplicates():
            df1 = volume_plan_tsm.loc[volume_plan_tsm['rev_group'].isin([category])].groupby(
                ['TOTAL', 'rev_group']).sum(numeric_only=True)

            df2 = volume_plan_tsm.loc[volume_plan_tsm['rev_group'].isin([category])].groupby(
                ['TOTAL', 'rev_pre_group']).sum(numeric_only=True)

            df_plan_total = pd.concat([df_plan_total, df1, df2])

        if not volume_fact.empty:

            df_fact_total = pd.DataFrame()

            for category in volume_fact['rev_group'].drop_duplicates():
                df1 = volume_fact.loc[volume_fact['rev_group'].isin([category])].groupby(
                    ['TOTAL', 'rev_group']).sum(numeric_only=True)

                df2 = volume_fact.loc[volume_fact['rev_group'].isin([category])].groupby(
                    ['TOTAL', 'rev_pre_group']).sum(numeric_only=True)

                df_fact_total = pd.concat([df_fact_total, df1, df2])

            df_total = df_plan_total.merge(df_fact_total,
                                           left_on=['TOTAL', 'rev_group'],
                                           right_on=['TOTAL', 'rev_group'],
                                           how='left').fillna(0).reset_index()
        else:
            df_fact_total = pd.DataFrame(columns=['rev_group', 'sum_sell', 'TOTAL'])

            df_total = df_plan_total.merge(df_fact_total,
                                           left_on=['TOTAL', 'rev_group'],
                                           right_on=['TOTAL', 'rev_group'],
                                           how='left').fillna(0)

        df_total = pd.concat([df_total,
                              df_total.loc[df_total['rev_group'].isin(['COFFEE',
                                                                       'Food&Diary',
                                                                       'CPW',
                                                                       'CONFECTIONERY',
                                                                       'PURINA'])].sum(numeric_only=True
                                                                                       ).rename('Total'
                                                                                                ).to_frame().T]).fillna(
            ''
        ).rename({'TOTAL': 'tier'},
                 axis=1)

        df_total['%'] = round((df_total['sum_sell'] / df_total['target']) * 100, 0
                              ).replace(np.nan, 0
                                        ).replace(np.inf, 100)

        df_total['%'] = df_total['%'].apply(lambda x: '{0:.0f}%'.format(x))

        df_total['Осталось'] = df_total['target'] - df_total['sum_sell']

        df_total['План на день'] = round(df_total['Осталось'] / work_day(), 2)

        df_list.insert(0, df_total.rename({'tier': 'TOTAL',
                                           'rev_group': 'Revision Group',
                                           'target': 'План',
                                           'sum_sell': 'Факт'}, axis=1).drop('id', axis=1))

        return df_list

    else:
        if not volume_fact.empty:

            df_fact_total = pd.DataFrame()

            for category in volume_fact['rev_group'].drop_duplicates():
                df1 = volume_fact.loc[volume_fact['rev_group'].isin([category])].groupby(
                    ['TOTAL', 'rev_group']).sum(numeric_only=True)

                df2 = volume_fact.loc[volume_fact['rev_group'].isin([category])].groupby(
                    ['TOTAL', 'rev_pre_group']).sum(numeric_only=True)

                df_fact_total = pd.concat([df_fact_total, df1, df2])

            df_total = df_fact_total.fillna(0).rename({'sum_sell': 'Факт'}, axis=1).reset_index()

            df_list.append(df_total.rename({'tier': 'TOTAL',
                                            'rev_group': 'Revision Group',
                                            'target': 'План',
                                            'sum_sell': 'Факт'}, axis=1))

            return df_list

        return df_list


# Функция формирования DatFrame по Топх
def df_topx(topx_plan, topx_fact, cat_topx):
    # Проверяем на наличие плана
    if not topx_plan.empty:

        df_plan = pd.DataFrame()

        for category in topx_plan['category'].drop_duplicates():
            df1 = topx_plan.loc[topx_plan['category'].isin([category])].groupby(['category']).sum(numeric_only=True)

            df2 = topx_plan.loc[topx_plan['category'].isin([category])].groupby(['dbc']).sum(numeric_only=True)

            df_plan = pd.concat([df_plan, df1, df2])

        df_plan = df_plan.reset_index()
        # Проверяем на наличие факта
        if not topx_fact.empty:

            # Группируем по DBC
            topx_fact = topx_fact.groupby(['code_tt_kis', 'rev_group_top', 'dbc']).sum(numeric_only=True).reset_index()

            # Подтягиваем категории топх, минимальный зачет, наименования DBC по DBC
            topx_fact = topx_fact.merge(cat_topx, left_on='dbc', right_on='dbc', how='left').fillna(0)

            # Определяем какие позиции прогружены до минимального порога зачета
            topx_fact['topx'] = np.where(topx_fact['count_piece'] >= topx_fact['min_sell'], 'ok', '')

            # Заменяем DBC дубликаты, пропуская не совпадающие.
            topx_fact['dbc'] = topx_fact['dbc'].map(DictMiss(dbc_replace))

            # Фильтруем фрейм по зачтенным позициям
            topx_fact = topx_fact.loc[topx_fact['topx'] == 'ok']

            # Группируем повторно по DBC, чтобы избавиться от дублирующих позиций
            topx_fact = topx_fact.groupby(['code_tt_kis', 'rev_group_top', 'dbc']).count().reset_index()

            # Удаляем не нужные столбцы
            topx_fact.drop(['code_tt_kis', 'count_piece', 'min_sell'], axis=1, inplace=True)

            df_fact = pd.DataFrame()

            # Группируем по каждой категории и DBC, цепляем список DBC под категорию.
            for category in topx_fact['rev_group_top'].drop_duplicates():
                df1 = topx_fact.loc[topx_fact['rev_group_top'].isin([category])].groupby(['rev_group_top']).count()

                df2 = topx_fact.loc[topx_fact['rev_group_top'].isin([category])].groupby(['dbc']).count()

                df_fact = pd.concat([df_fact, df1, df2])

            df_fact = df_fact.reset_index().drop(['dbc', 'rev_group_top', 'dbc_name'], axis=1)

            # Подтягиваем факт к планам
            df_res = df_plan.merge(df_fact, left_on=['index'], right_on=['index'],
                                   how='left').fillna(0).rename({'target': 'План',
                                                                 'topx': 'Факт',
                                                                 'index': 'Категория'}, axis=1)

            rev_group_top = ['COFFEE', 'CONFECTIONERY', 'CPW', 'CULINARY', 'Nesquik', 'PURINA']

            # Добавляем ТОТАЛ по всем категориям
            df_res = pd.concat([df_res, df_res.loc[
                df_res['Категория'].isin(rev_group_top)].sum(numeric_only=True
                                                             ).rename('Total'
                                                                      ).to_frame().T]).fillna('')

            # Меняем DBC на DBC_name пропуская наименования категорий
            df_res['Категория'] = df_res['Категория'].map(DictMiss(cat_topx.set_index('dbc')['dbc_name']))

            df_res['%'] = round((df_res['Факт'] / df_res['План']) * 100, 2).replace(np.nan, 0).replace(np.inf, 100)

            df_res['%'] = df_res['%'].apply(lambda x: '{0:.2f}%'.format(x))

            df_res['Осталось'] = df_res['План'] - df_res['Факт']

            df_res['План на день'] = round(df_res['Осталось'] / work_day(), 0)

            return df_res.drop('id', axis=1)

        # Если есть план, но нет факта, содаем пустой фрейм данных для факта
        else:
            df_fact = pd.DataFrame(columns=['index', 'topx'])

            df_res = df_plan.merge(df_fact, left_on=['index'], right_on=['index'],
                                   how='left').fillna(0).rename({'target': 'План',
                                                                 'topx': 'Факт',
                                                                 'index': 'Категория'}, axis=1)
            rev_group_top = ['COFFEE', 'CONFECTIONERY', 'CPW', 'CULINARY', 'Nesquik', 'PURINA']

            df_res = pd.concat([df_res, df_res.loc[
                df_res['Категория'].isin(rev_group_top)].sum(numeric_only=True
                                                             ).rename('Total'
                                                                      ).to_frame().T]).fillna('')

            # Меняем DBC на DBC_name пропуская наименования категорий
            df_res['Категория'] = df_res['Категория'].map(DictMiss(cat_topx.set_index('dbc')['dbc_name']))

            df_res['%'] = round((df_res['Факт'] / df_res['План']) * 100, 2).replace(np.nan, 0).replace(np.inf, 100)

            df_res['%'] = df_res['%'].apply(lambda x: '{0:.2f}%'.format(x))

            df_res['Осталось'] = df_res['План'] - df_res['Факт']

            df_res['План на день'] = round(df_res['Осталось'] / work_day(), 0)

            return df_res.drop('id', axis=1)
    else:
        # Если нет плана, проверям факт, если есть факт то формируем факт и возвращаем
        if not topx_fact.empty:

            topx_fact = topx_fact.groupby(['code_tt_kis', 'rev_group_top', 'dbc']).sum(numeric_only=True).reset_index()

            topx_fact = topx_fact.merge(cat_topx, left_on='dbc', right_on='dbc', how='left').fillna(0)
            topx_fact['topx'] = np.where(topx_fact['count_piece'] >= topx_fact['min_sell'], 'ok', '')
            topx_fact['dbc'] = topx_fact['dbc'].map(DictMiss(dbc_replace))
            topx_fact = topx_fact.loc[topx_fact['topx'] == 'ok']

            topx_fact = topx_fact.groupby(['code_tt_kis', 'rev_group_top', 'dbc']).count().reset_index()

            topx_fact.drop(['code_tt_kis', 'count_piece', 'min_sell'], axis=1, inplace=True)
            df_fact = pd.DataFrame()

            for category in topx_fact['rev_group_top'].drop_duplicates():
                df1 = topx_fact.loc[topx_fact['rev_group_top'].isin([category])].groupby(['rev_group_top']).count()

                df2 = topx_fact.loc[topx_fact['rev_group_top'].isin([category])].groupby(['dbc']).count()

                df_fact = pd.concat([df_fact, df1, df2])

            df_res = df_fact.reset_index().drop(['dbc', 'rev_group_top', 'dbc_name'], axis=1)

            df_res = df_res.rename({'topx': 'Факт', 'index': 'Категория'}, axis=1)

            df_res['Категория'] = df_res['Категория'].map(DictMiss(cat_topx.set_index('dbc')['dbc_name']))

            return df_res

        else:
            # Если нет плани и факта, возвращаем пустой фрейм данных
            df_res = pd.DataFrame()

            return df_res


def df_coverage(cov_plan, cov_fact, user, tt_list) -> list:
    def cov_dont_work(tt, fact):
        try:
            df = tt.merge(fact,
                          left_on='kis_code',
                          right_on='code_tt_kis',
                          how='left').fillna(0)
            df = df.loc[df['sum_sell'] < 1500].sort_values('sum_sell', ascending=False
                                                           ).drop('kis_code', axis=1)

            df = df[['tt_id__tt', 'address', 'sum_sell']].rename({'tt_id__tt': 'Наименование ТТ',
                                                                  'address': 'Адрес ТТ',
                                                                  'sum_sell': 'Сумма продаж'}, axis=1)
        except KeyError:
            tt['sum_sell'] = 0
            df = tt[['tt_id__tt', 'address', 'sum_sell']].rename({'tt_id__tt': 'Наименование ТТ',
                                                                  'address': 'Адрес ТТ',
                                                                  'sum_sell': 'Сумма продаж'}, axis=1)

        return df

    if not cov_plan.empty:
        terr = cov_plan.loc[0, user]

        df_plan = cov_plan.groupby([user]).sum(numeric_only=True)
    else:
        df_fact = cov_fact.groupby([user, 'code_tt_kis']).sum(numeric_only=True)

        tt_list = cov_dont_work(tt_list, df_fact)

        df_fact['status'] = np.where(df_fact['sum_sell'] >= 1500, 'ok', '')

        df_fact = df_fact.loc[df_fact['status'] == 'ok'].reset_index().drop(['code_tt_kis', 'sum_sell'], axis=1
                                                                            ).rename({'status': 'Факт'}, axis=1)
        df_fact = df_fact.groupby([user]).count()

        return [df_fact, tt_list]

    if not cov_fact.empty:
        df_fact = cov_fact.groupby([user, 'code_tt_kis']).sum(numeric_only=True)

        tt_list = cov_dont_work(tt_list, df_fact)

        df_fact['status'] = np.where(df_fact['sum_sell'] >= 1500, 'ok', '')

        df_fact = df_fact.loc[df_fact['status'] == 'ok'].reset_index().drop(['code_tt_kis', 'sum_sell'], axis=1)

        df_fact = df_fact.groupby([user]).count()
    else:
        df_fact = pd.DataFrame({user: [terr], 'status': [0]})

        df_fact = df_fact.groupby([user]).sum(numeric_only=True)

        tt_list = cov_dont_work(tt_list, df_fact)

    df_res = df_plan.merge(df_fact, on=user, how='left')

    if len(df_res.index) > 1:
        df_res.loc['ИТОГО'] = df_res.sum(numeric_only=True)

    df_res['%'] = round((df_res['status'] / df_res['target']) * 100, 2).replace(np.nan, 0).replace(np.inf, 100)

    df_res['%'] = df_res['%'].apply(lambda x: '{0:.2f}%'.format(x))

    df_res['Осталось'] = df_res['target'] - df_res['status']

    df_res['План на день'] = round(df_res['Осталось'] / work_day(), 0)

    df_res = df_res.reset_index().rename({user: 'Территория', 'target': 'План', 'status': 'Факт'}, axis=1)

    return [df_res, tt_list]
