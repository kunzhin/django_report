from django.conf import settings
from report_audit_control.connection_db import engine, sqlcol
import pandas as pd
import numpy as np
import os
from datetime import datetime
from sqlalchemy import text
from report_audit_control.date_work import current_month, previous_month
from .func import send_telegram
from .models import ClientException


def update_770(message):
    try:
        start_time = datetime.now()

        path_770 = os.path.join(settings.BASE_DIR, 'media', 'indicators', 'report_770')

        file_list_770 = os.listdir(path_770)

        report_770 = pd.DataFrame()

        for file in file_list_770:
            file_path = os.path.join(path_770, file)
            df = pd.read_excel(file_path)
            report_770 = pd.concat([report_770, df])

        report_770 = report_770.loc[report_770['Месяц'].isin([current_month(), previous_month()])]

        report_770['Статус'] = np.where(
            (report_770['Клиенту отгружен продукт по сниженной цене согласно Программы (Да\Нет)'] == 'Да') & (
                    report_770['Ссылки на фотопоток'] != 'фотографий не найдено'), 1, 0)

        report_770['Категория'] = report_770['Категория'].replace(
            {'Полка кофе': 'Усиление Кофе', 'Хот Зона (миксы)': 'Усиление Кофе', 'Кулинария': 'Усиление Магги',
             'Пурина': 'Усиление Пурина'})

        report_770 = report_770[['Месяц', 'Дата создания Фотографий / совершения визита', 'Канал ТТ', 'Вывеска сети',
                                 'Площадка', 'RSM', 'DSM', 'TSM', 'Имя ТП', 'Код ТТ', 'Название ТТ', 'Адрес ТТ',
                                 'Категория', 'Клиенту отгружен продукт по сниженной цене согласно Программы (Да\Нет)',
                                 'Является ли магазин стандартным. (Да\Нет)', 'Ссылки на фотопоток', 'Статус']]

        report_770 = report_770.rename({'Дата создания Фотографий / совершения визита': 'Дата документа',
                                        'Имя ТП': 'ESR',
                                        'Клиенту отгружен продукт по сниженной цене согласно Программы (Да\Нет)': 'Статус снижения цены',
                                        'Является ли магазин стандартным. (Да\Нет)': 'Стандартный магазин',
                                        'Ссылки на фотопоток': 'URL'}, axis=1)

        # Очищаем таблицу полностью
        with engine.connect() as connection:
            connection.execute(text("SET FOREIGN_KEY_CHECKS=0"))
            connection.execute(text("TRUNCATE TABLE `indicators_report770`"))

        outputdict = sqlcol(report_770)

        report_770.to_sql('indicators_report770', con=engine, if_exists='append', index=False, dtype=outputdict)

        time = datetime.now() - start_time

        if message == 'on':
            message = 'Данные по фотопотоку обновлены.'

            send_telegram(message)

        return time

    except Exception as err:
        return err


def update_145():
    try:
        start_time = datetime.now()

        path_145 = os.path.join(settings.BASE_DIR, 'media', 'indicators', 'report145')
        file_list_145 = os.listdir(path_145)

        report_145 = pd.DataFrame()

        for file in file_list_145:
            file_path = os.path.join(path_145, file)
            df = pd.read_excel(file_path)
            report_145 = pd.concat([report_145, df])

        report_145 = report_145[['Наименование площадки', 'RSM', 'DSM', 'TSM', 'Имя ESR', 'ID ТТ', 'XCRM GUID',
                                 'Название ТТ', 'Адрес', 'Канал ТТ', 'Tier', 'Ассортимент', 'DBC ID',
                                 'Наименование DBC', 'Месяц', 'Объем продаж точки']]

        report_145['Tier'].fillna('Tier TT', inplace=True)

        month = str(report_145['Месяц'].drop_duplicates().values[0])

        client_except = pd.DataFrame(ClientException.objects.all().values('code_tt', 'status')
                                     ).rename({'code_tt': 'ID ТТ', 'status': 'Purina_except'}, axis=1
                                              ).astype({'ID ТТ': 'int64'})

        report_145 = report_145.merge(client_except, left_on='ID ТТ', right_on='ID ТТ', how='left').drop_duplicates()

        # Удаляем данные из таблицы за период обновляемого отчета
        # with engine.connect() as connection:
        #     connection.execute(
        #         text(f"DELETE FROM `indicators_report145` WHERE `Месяц` = '{month}'"))

        # Очищаем таблицу полностью
        with engine.connect() as connection:
            connection.execute(text("SET FOREIGN_KEY_CHECKS=0"))
            connection.execute(text("TRUNCATE TABLE `indicators_report145`"))

        outputdict = sqlcol(report_145)

        report_145.to_sql('indicators_report145', con=engine, if_exists='append', index=False, dtype=outputdict)

        # message = 'Отчеты обновлены. ' \
        #           'Информация находится по адресу: http://promo-ap.ru:8000. ' \
        #           'Для доступа: Логин esrtest, Пароль Zaq12wsX!'
        #
        # send_telegram(message)

        time = datetime.now() - start_time

        return time

    except Exception as err:
        return err


def update_07(message):
    try:
        start_time = datetime.now()

        path_07 = os.path.join(settings.BASE_DIR, 'media', 'indicators', 'report07')
        file_list_07 = os.listdir(path_07)

        report_07 = pd.DataFrame()

        for file in file_list_07:
            file_path = os.path.join(path_07, file)
            df = pd.read_excel(file_path,
                               converters={'дата документа': pd.to_datetime, 'дата отгрузки': pd.to_datetime})
            report_07 = pd.concat([report_07, df])

        cat_topx = pd.read_sql('indicators_topcategory', con=engine)
        cat_topx.drop('id', axis=1, inplace=True)

        cat_vol = pd.read_sql('indicators_volumecategory', con=engine)
        cat_vol.drop('id', axis=1, inplace=True)

        report_07 = report_07[['Площадка', 'RSM', 'DSM', 'TSM', 'ESR', 'Tier',
                               'Стрим ТК', 'виртуальность', 'код ТТ КИС', 'код ТТ', 'наименование ТТ', 'адрес ТТ',
                               'Специализация ТТ', 'канал ТТ', 'Ключевая розница', 'Ключевой опт',
                               'сеть', 'номер документа', 'дата документа', 'дата отгрузки',
                               'тип документа', 'месяц', 'Неделя', 'день', 'DBC',
                               'наименование DBC', 'код товара', 'товар', 'категория', 'группа',
                               'подгруппа', 'Сумма продаж (руб.)', 'Сумма продаж БЕЗ НДС (руб.)',
                               'Количество (шт.)', 'Вес (кг.)']]

        report_07['Price'] = report_07['Сумма продаж (руб.)'] / report_07['Количество (шт.)']

        report_07 = report_07.merge(cat_vol, left_on=['группа'], right_on=['группа'], how='left')
        report_07 = report_07.merge(cat_topx[['DBC', 'RevGroupTopX', 'Min_sell']],
                                    left_on=['DBC'],
                                    right_on=['DBC'],
                                    how='left').sort_values(by=['дата отгрузки'], ascending=True)

        report_07['TOP'] = np.where(report_07['Количество (шт.)'] >= report_07['Min_sell'], 'ok', '')

        # Меняем месяц, неделю, день по дате отгрузки
        report_07['месяц'] = report_07['дата отгрузки'].dt.month
        report_07['Неделя'] = report_07['дата отгрузки'].dt.week
        report_07['день'] = report_07['дата отгрузки'].dt.day

        start_day = str(report_07['дата отгрузки'].min())
        end_day = str(report_07['дата отгрузки'].max())

        # Удаляем данные из таблицы за период обновляемого отчета
        with engine.connect() as connection:
            connection.execute(
                text(f"DELETE FROM `indicators_report07` WHERE `дата отгрузки` BETWEEN '{start_day}' AND '{end_day}'"))

        outputdict = sqlcol(report_07)

        report_07.to_sql('indicators_report07', con=engine, if_exists='append', index=False, dtype=outputdict)

        time = datetime.now() - start_time

        if message == 'on':
            message = 'Отчеты по продажам обновлены. ' \
                      'Информация находится по адресу: http://promo-ap.ru:8000. ' \
                      'Для доступа используйте личный Логин/Пароль'

            send_telegram(message)

        return time

    except Exception as err:
        return err
