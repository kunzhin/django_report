from django.conf import settings
from report_audit_control.connection_db import engine, sqlcol
import pandas as pd
import numpy as np
import os
from datetime import datetime
from report_audit_control.date_work import previous_day_month, today
from sqlalchemy import text
from indicators.func import send_telegram

CITY = {'nkz': 'Новокузнецк', 'nsk': 'Новосибирск', 'krs': 'Красноярск', 'abk': 'Абакан', 'omsk': 'Омск'}

PATH_AREA = ['nkz', 'abk', 'krs', 'nsk', 'omsk']


def formation_remains(place):
    print(place)
    remains = os.path.join(settings.BASE_DIR,
                           'media',
                           'remains',
                           place,
                           'remains_' + place + '.xls')

    transits = os.path.join(settings.BASE_DIR,
                            'media',
                            'remains',
                            place,
                            'transit_' + place + '.xls')

    remains_expiration_dates = os.path.join(settings.BASE_DIR,
                                            'media',
                                            'remains',
                                            place,
                                            'expiration_' + place + '.xls')

    category_remains_df = pd.read_sql('remains_categoryremains', con=engine)

    # Читаем данные
    remains_df = pd.read_excel(remains, skiprows=[0, 1, 2], header=[1])
    transits_df = pd.read_excel(transits, skiprows=[0], header=0, converters={'Код': str})
    remains_expiration_dates_df = pd.read_excel(remains_expiration_dates, skiprows=[0, 1, 2], header=[0])

    # print(remains_df)
    # Готовим остатки
    if (place == 'krs') | (place == 'abk'):

        remains_df = remains_df[['Код', 'Артикул ', 'Номенклатура', 'БИ.3', 'Unnamed: 12']]

        remains_df = remains_df.dropna(subset=['Номенклатура', 'Артикул ']
                                       ).reset_index(
        ).rename(columns={'БИ.3': 'Остаток', 'Unnamed: 12': 'Резерв', 'Артикул ': 'Артикул'})

    else:
        remains_df = remains_df.dropna(subset=['Номенклатура', 'Артикул ']
                                       ).reset_index(
        ).drop(['index', 'БИ', 'БИ.1', 'БИ.2', 'Unnamed: 7'], axis=1
               ).rename(columns={'БИ.3': 'Остаток', 'Unnamed: 8': 'Резерв', 'Артикул ': 'Артикул'})

    remains_df['Резерв'] = remains_df['Резерв'].fillna(0)

    remains_df['Свободный остаток'] = remains_df['Остаток'] - remains_df['Резерв']

    # Готовим остатки по срокам
    remains_expiration_dates_df = remains_expiration_dates_df[['Артикул',
                                                               'Дата окончания срока годности',
                                                               'Unnamed: 14']
    ].dropna(subset=['Дата окончания срока годности']
             ).rename(columns={'Unnamed: 14': 'Остаток срока',
                               'Дата окончания срока годности': 'Срок годности'}
                      ).drop_duplicates(['Артикул'])

    remains_expiration_dates_df = remains_expiration_dates_df.reset_index(
    ).drop(columns=['index'])

    # Готовим Транзиты
    try:
        transits_df = transits_df.dropna(subset=['Код', 'DBC']
                                         ).reset_index().drop(['index',
                                                               'DBC',
                                                               'Остаток (Короб)'], axis=1)
        transits_df['Артикул'] = transits_df['Артикул'].astype(float, errors='raise')
    except:
        transits_df = pd.DataFrame(columns=['Артикул', 'Код', 'DBC', 'Номенклатура', 'Дата прихода', 'Транзит (Короб)', 'Остаток (Короб)'])


    # Читаем SAP топх позиций
    topx = pd.read_sql(
        f"SELECT DISTINCT `код товара`, `TOP` FROM indicators_report07 WHERE `виртуальность`='Реальный' AND `дата отгрузки` BETWEEN '{previous_day_month(2)}' AND '{today()}'",
        con=engine).rename({'код товара': 'Артикул', 'TOP': 'TOPX'}, axis=1).replace({'ok': 'topx'})

    topx = topx.loc[topx['TOPX'] == 'topx'].drop_duplicates(subset=['Артикул'])

    status_sap = pd.read_sql(
        f"SELECT `код товара`, `status` FROM remains_suspended", con=engine
    ).rename({'код товара': 'Артикул'}, axis=1).astype({'Артикул': 'float64'}, errors='ignore')

    launch = pd.read_sql(
        f"SELECT `код товара`, `launch` FROM remains_launch", con=engine
    ).rename({'код товара': 'Артикул'}, axis=1).astype({'Артикул': 'float64'}, errors='ignore')

    # Подтягиваем сроки и транзиты к остаткам
    remains_result = remains_df.merge(remains_expiration_dates_df, left_on=['Артикул'], right_on=['Артикул'], how='left')

    remains_result = remains_result.merge(transits_df,
                                          left_on=['Артикул', 'Код', 'Номенклатура'],
                                          right_on=['Артикул', 'Код', 'Номенклатура'],
                                          how='outer')

    remains_result = remains_result.merge(topx, left_on=['Артикул'], right_on=['Артикул'], how='left').replace(np.nan, '')

    remains_result = remains_result.merge(status_sap, left_on=['Артикул'], right_on=['Артикул'], how='left').replace(np.nan, '')

    remains_result = remains_result.merge(launch, on=['Артикул'], how='left')

    remains_result['Город'] = CITY[place]

    remains_result = remains_result.astype(
        {'Артикул': 'int64', 'Остаток': 'int64', 'Резерв': 'int64', 'Свободный остаток': 'int64',
         'Транзит (Короб)': 'int64'}, errors='ignore')
    remains_result['Код категории'] = remains_result['Код'].apply(lambda x: x[:3])

    remains_result = remains_result.merge(category_remains_df, left_on='Код категории', right_on='Код категории',
                                          how='left')
    remains_result['Остаток срока'] = remains_result['Остаток срока'].apply(lambda x: '{0} %'.format(x))
    remains_result.index += 1  # Начинаем индексацию с еденицы
    remains_result = remains_result[['Код категории',
                                     'Категория',
                                     'Код',
                                     'Артикул',
                                     'Номенклатура',
                                     'Остаток',
                                     'Резерв',
                                     'Свободный остаток',
                                     'Срок годности',
                                     'Остаток срока',
                                     'Дата прихода',
                                     'Транзит (Короб)',
                                     'Город',
                                     'TOPX',
                                     'status',
                                     'launch']].replace(0, '')

    return remains_result


def update_data_remains(message):
    # try:
    start_time = datetime.now()

    remains_result = pd.DataFrame()

    for place in PATH_AREA:
        remains = formation_remains(place)
        remains_result = pd.concat([remains_result, remains])

    with engine.connect() as connection:
        connection.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        connection.execute(text("TRUNCATE TABLE `remains_remains`"))

    outputdict = sqlcol(remains_result)
    remains_result.to_sql('remains_remains', con=engine, if_exists='append', index=False, dtype=outputdict)

    time = datetime.now() - start_time

    if message == 'on':
        message = 'Обновлены остатки по всем площадкам'

        send_telegram(message)

    return time

    # except Exception as err:
    #    return err
