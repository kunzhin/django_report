import time
import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
from pandas.tseries.offsets import MonthEnd, MonthBegin, BMonthBegin, BMonthEnd

MONTH_DICT = {'January': 'Январь',
              'February': 'Февраль',
              'March': 'Март',
              'April': 'Апрель',
              'May': 'Май',
              'June': 'Июнь',
              'July': 'Июль',
              'August': 'Август',
              'September': 'Сентябрь',
              'October': 'Октябрь',
              'November': 'Ноябрь',
              'December': 'Декабрь'}

MONTH_NUMBER = {'Январь': 1,
                'Февраль': 2,
                'Март': 3,
                'Апрель': 4,
                'Май': 5,
                'Июнь': 6,
                'Июль': 7,
                'Август': 8,
                'Сентябрь': 9,
                'Октябрь': 10,
                'Ноябрь': 11,
                'Декабрь': 12}

NUMBER_MONTH = {1: 'Январь',
                2: 'Февраль',
                3: 'Март',
                4: 'Апрель',
                5: 'Май',
                6: 'Июнь',
                7: 'Июль',
                8: 'Август',
                9: 'Сентябрь',
                10: 'Октябрь',
                11: 'Ноябрь',
                12: 'Декабрь'}

DAY_ROUTE = {1: 'ПН', 2: 'ВТ', 3: 'СР', 4: 'ЧТ', 5: 'ПТ', 6: 'СБ', 7: 'ВС'}                


# Узнаем текущий месяц
def date():
    month = time.strftime('%B')
    return month


# Присваиваем русское наименование месяца
def current_month():
    return MONTH_DICT[date()]


def previous_month(months=1):
    x = datetime.datetime.today()
    x = (x - relativedelta(months=months)).strftime('%B')
    return MONTH_DICT[x]


def today():
    day: str = time.strftime('%Y-%m-%d')
    return day


# Возрат даты несколько месяцев назад
def previous_day_month(count_month):
    today = datetime.datetime.today()
    date = (today - relativedelta(months=count_month)).strftime('%Y-%m-%d')
    return date


# Последний рабочий день месяца
def day_end():
    return BMonthEnd().rollforward(today())


# Первый рабочий день месяца
def day_begin():
    month = current_month()
    if month == 'Январь':
        day_begin = pd.Timestamp('2023-01-09')
    else:
        day_begin = BMonthBegin().rollback(today())
    return day_begin


# Прошло рабочих дней
def passed_work_day():
    correction = 0 #
    month = current_month()
    if month == 'Январь':
        correction = 1

    passed_work_day = int(pd.date_range(day_begin(), today(), freq='B').value_counts().count() - correction)

    if passed_work_day == 0:
        passed_work_day = 1
    return passed_work_day


# Кол-во рабочих дней
def work_day_in_month():
    correction = 2 # Корректировка на Декабрь
    work_day_in_month = int(pd.date_range(day_begin(), day_end(), freq='B').value_counts().count()) - correction
    return work_day_in_month


# Прошло времени
def time_passed():
    return '{0:.0f}'.format((passed_work_day() / work_day_in_month()) * 100)
    # return '{0:.0f}%'.format(100)


# Осталось рабочих дней
def work_day():
    work_days = int(pd.date_range(today(), day_end(), freq='B').value_counts().count() - 1)
    if work_days == 0:
        work_days = 1
    return work_days


# Последняя дата месяца
def day_end_month(day=today()):
    return pd.Timestamp(MonthEnd().rollforward(day))


# Первая дата месяца
def day_begin_month(day=today()):
    return pd.Timestamp(MonthBegin().rollback(day))
