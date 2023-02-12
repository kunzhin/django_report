from report_audit_control.connection_db import engine, sqlcol
import pandas as pd
from sqlalchemy import text
from datetime import datetime
from report_audit_control.date_work import previous_day_month, today, DAY_ROUTE
from .models import *


def hierarchy():
    try:
        start_time = datetime.now()
        data = pd.DataFrame(ESR.objects.all().values('esr', 'tsm_id__tsm', 'tsm_id__dsm_id__dsm'))
        data['RSM'] = 'GC_Сибирь_Континент_SM'
        data = data.rename({'esr': 'ESR', 'tsm_id__tsm': 'TSM', 'tsm_id__dsm_id__dsm': 'DSM'}, axis=1)[['RSM', 'DSM', 'TSM', 'ESR']]

        with engine.connect() as connection:
            connection.execute(text("SET FOREIGN_KEY_CHECKS=0;"))
            connection.execute(text("TRUNCATE TABLE `accounts_hierarchy`"))

        outputdict = sqlcol(data)

        data.to_sql('accounts_hierarchy', con=engine, if_exists='append', index=False, dtype=outputdict)

        time = datetime.now() - start_time

        return time

    except Exception as err:
        return err


def update_tt_address():
    try:
        start_time = datetime.now()

        # Обновление наименования ТТ за последние 4 месяца
        esr_id = pd.read_sql('accounts_esr', con=engine)
        #tt = pd.read_sql(
        #    f"SELECT DISTINCT `наименование ТТ`, `ESR` FROM indicators_report07 WHERE `виртуальность`='Реальный' AND `дата отгрузки` BETWEEN '{previous_day_month(4)}' AND '{today()}'",
        #    con=engine)

        tt = pd.read_sql(
            f"SELECT DISTINCT `наименование ТТ`, `ESR` FROM indicators_report07 WHERE `дата отгрузки` BETWEEN '{previous_day_month(4)}' AND '{today()}'",
            con=engine)

        tt_name_id = tt.merge(esr_id, left_on='ESR', right_on='ESR', how='left').drop(['ESR', 'tsm_id'], axis=1).rename(
            {'id': 'esr_id'}, axis=1).dropna().sort_values(by=['наименование ТТ'])

        with engine.connect() as connection:
            connection.execute(text("SET FOREIGN_KEY_CHECKS=0;"))
            connection.execute(text("TRUNCATE TABLE `accounts_tt`"))

        outputdict = sqlcol(tt_name_id)

        tt_name_id.to_sql('accounts_tt', con=engine, if_exists='append', index=False, dtype=outputdict)

        # Обновление адресов ТТ за последние 4 месяца
        tt_id = pd.read_sql('accounts_tt', con=engine)
        #tt_address = pd.read_sql(
        #    f"SELECT DISTINCT `код ТТ`, `код ТТ КИС`, `адрес ТТ`, `наименование ТТ`, `дата документа` FROM indicators_report07 WHERE `виртуальность`='Реальный' AND `дата отгрузки` BETWEEN '{previous_day_month(4)}' AND '{today()}'",
        #    con=engine).drop_duplicates(subset=['код ТТ'], keep='last')

        tt_address = pd.read_sql(
            f"SELECT DISTINCT `код ТТ`, `код ТТ КИС`, `Tier`, `канал ТТ`, `адрес ТТ`, `наименование ТТ`, `дата документа` FROM indicators_report07 WHERE `дата отгрузки` BETWEEN '{previous_day_month(4)}' AND '{today()}'",
            con=engine).drop_duplicates(subset=['код ТТ'], keep='last')

        tt_address['дата документа'] = tt_address['дата документа'].apply(lambda x: DAY_ROUTE[datetime.isoweekday(x)])

        tt_address_id = tt_address.merge(tt_id, left_on='наименование ТТ', right_on='наименование ТТ', how='left').drop(
            ['наименование ТТ', 'esr_id'], axis=1
            ).rename({'id': 'tt_id',
            'дата документа': 'day_route'}, axis=1).dropna().sort_values(by=['day_route'])

        with engine.connect() as connection:
            connection.execute(text("SET FOREIGN_KEY_CHECKS=0;"))
            connection.execute(text("TRUNCATE TABLE `accounts_address`"))

        outputdict = sqlcol(tt_address_id)

        tt_address_id.to_sql('accounts_address', con=engine, if_exists='append', index=False, dtype=outputdict)

        time = datetime.now() - start_time
        return time

    except Exception as err:
        return err
