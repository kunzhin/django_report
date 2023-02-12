import numpy as np
from django.conf import settings
from report_audit_control.connection_db import engine, sqlcol
import pandas as pd
import os
from datetime import datetime
from sqlalchemy import text
from .func import send_telegram


def update_plan(message):
    try:
        start_time = datetime.now()

        file_plans = os.path.join(settings.BASE_DIR, 'media', 'indicators', 'xls_plan', 'update_plan.xlsx')

        rev_cat_vol = pd.read_sql('indicators_volumecategory', con=engine).drop(['id', 'группа'], axis=1).drop_duplicates()

        # Читаем планы объема по ТСМ
        volume_tsm_plan = pd.read_excel(file_plans, sheet_name='target_vol_tsm')

        volume_tsm_plan = volume_tsm_plan.merge(rev_cat_vol, left_on='RevPreGroup', right_on='RevPreGroup',
                                                how='left').dropna()

        with engine.connect() as connection:
            connection.execute(text("SET FOREIGN_KEY_CHECKS=0"))
            connection.execute(text("TRUNCATE TABLE `indicators_volumeplantsm`"))

        outputdict = sqlcol(volume_tsm_plan)
        volume_tsm_plan.to_sql('indicators_volumeplantsm', con=engine, if_exists='append', index=False, dtype=outputdict)

        # Читаем планы объема по ЕСР
        volume_esr_plan = pd.read_excel(file_plans, sheet_name='target_vol_esr')

        vol_esr = volume_esr_plan.merge(rev_cat_vol, left_on='RevPreGroup', right_on='RevPreGroup', how='left').dropna()

        vol_esr_tier3 = vol_esr[['ESR', 'RevPreGroup', 'Revision Group', 'Tier 3']
        ].rename({'Tier 3': 'Target'}, axis=1
                 )

        vol_esr_tiertt = vol_esr[['ESR', 'RevPreGroup', 'Revision Group', 'Tier TT']
        ].rename({'Tier TT': 'Target'}, axis=1
                 )

        vol_esr_tier_whs = vol_esr[['ESR', 'RevPreGroup', 'Revision Group', 'Tier Wholesale']
        ].rename({'Tier Wholesale': 'Target'}, axis=1
                 )

        vol_esr_tiertt.insert(loc=1, column='Tier', value='Tier TT')
        vol_esr_tier3.insert(loc=1, column='Tier', value='Tier 3')
        vol_esr_tier_whs.insert(loc=1, column='Tier', value='Tier Wholesale')

        volume_esr_plan = round(pd.concat([vol_esr_tiertt, vol_esr_tier3, vol_esr_tier_whs]), 2)

        with engine.connect() as connection:
            connection.execute(text("SET FOREIGN_KEY_CHECKS=0"))
            connection.execute(text("TRUNCATE TABLE `indicators_volumeplanesr`"))

        outputdict = sqlcol(volume_esr_plan)
        volume_esr_plan.to_sql('indicators_volumeplanesr', con=engine, if_exists='append', index=False, dtype=outputdict)

        # Читаем планы топх по ЕСР
        topx_plan = pd.read_excel(file_plans, sheet_name='cat_topx_plan')
        terr_list = pd.read_sql(
            f"SELECT DISTINCT `RSM`, `DSM`, `TSM`, `ESR` FROM accounts_hierarchy",
            con=engine)

        topx_plan_result = topx_plan.groupby(by=['Категория', 'DBC', 'наименование DBC']).sum().stack().reset_index().rename(
            {'level_3': 'ESR', 0: 'Target'}, axis=1)

        topx_plan_result = topx_plan_result.merge(terr_list.drop(['RSM'], axis=1), left_on='ESR', right_on='ESR', how='left')

        # print(topx_plan_result[topx_plan_result.isnull().any(1)])

        with engine.connect() as connection:
            connection.execute(text("SET FOREIGN_KEY_CHECKS=0"))
            connection.execute(text("TRUNCATE TABLE `indicators_topplan`"))

        outputdict = sqlcol(topx_plan_result)

        topx_plan_result.to_sql('indicators_topplan', con=engine, if_exists='append', index=False, dtype=outputdict)

        # Читаем планы покрытия по ЕСР
        cov = pd.read_excel(file_plans, sheet_name='coverage')
        cov = cov.merge(terr_list.drop(['RSM'], axis=1), left_on='ESR', right_on='ESR', how='left')

        # print(cov[cov.isnull().any(1)])

        with engine.connect() as connection:
            connection.execute(text("SET FOREIGN_KEY_CHECKS=0"))
            connection.execute(text("TRUNCATE TABLE `indicators_coverageplan`"))

        outputdict = sqlcol(cov)

        cov.to_sql('indicators_coverageplan', con=engine, if_exists='append', index=False, dtype=outputdict)

        # Читаем планы по Усилениям
        target_task = pd.read_excel(file_plans, sheet_name='streng', index_col=[0])

        target_task = target_task.stack().reset_index().rename({'level_1': 'distr_task', 0: 'Target'}, axis=1)
        target_task = target_task.merge(terr_list, on='ESR', how='left')

        with engine.connect() as connection:
            connection.execute(text("SET FOREIGN_KEY_CHECKS=0"))
            connection.execute(text("TRUNCATE TABLE `indicators_distrtaskplan`"))

        outputdict = sqlcol(target_task)

        target_task.to_sql('indicators_distrtaskplan', con=engine, if_exists='append', index=False, dtype=outputdict)

        # Читаем планы по дистрибуционным задачам
        target_task = pd.read_excel(file_plans, sheet_name='i2l', header=[0, 1], index_col=[0]).fillna(0)

        target_task = target_task.stack(level=[0, 1]).reset_index().rename({'level_0': 'ESR',
                                                                            'level_1': 'distr_task',
                                                                            'level_2': 'view_task',
                                                                            0: 'Target'}, axis=1)
        target_task = target_task.merge(terr_list, on='ESR', how='left')

        with engine.connect() as connection:
            connection.execute(text("SET FOREIGN_KEY_CHECKS=0"))
            connection.execute(text("TRUNCATE TABLE `indicators_i2ltaskplan`"))

        outputdict = sqlcol(target_task)

        target_task.to_sql('indicators_i2ltaskplan', con=engine, if_exists='append', index=False, dtype=outputdict)

        time = datetime.now() - start_time

        if message == 'on':
            message = 'Планы обновлены'

            send_telegram(message)

        return time

    except Exception as err:
        return err
