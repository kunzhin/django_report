import pandas as pd
import numpy as np
from report_audit_control.date_work import today, previous_day_month

from .models import Remains
from indicators.models import Report07

PLACE = {
    'Абакан': 'SIB-Континент (Абакан)',
    'Красноярск': 'SIB-Континент (Красноярск)',
    'Новокузнецк': 'SIB-Континент (Новокузнецк)',
    'Новосибирск': 'SIB-Континент (Новосибирск)',
    'Омск': 'SIB-Континент (Омск)'
}


class SKU(object):
    def __init__(self, sap):
        self.sap = sap

    def move(self):
        move = pd.DataFrame(Report07.objects.filter(code_nestle=self.sap,
                                                    document_date__range=(previous_day_month(1), today())
                                                    ).values('region', 'document_date', 'product', 'count_piece'))
        if len(move.index) > 1:
            move = pd.pivot_table(move,
                                  columns='region',
                                  index='document_date',
                                  values='count_piece',
                                  aggfunc='sum',
                                  fill_value=0,
                                  )

            move.loc['ИТОГО'] = move.sum(numeric_only=True)

            move = move.reset_index().rename({'document_date': 'Дата'}, axis=1)

            move.columns.names = [None]

            return move

        else:
            return None


def contlog_remains(remains):
    # Доп.столбец дата транзита + кол-во коробов
    # remains['_dt'] = np.where((remains['date_arrival'] != '') & (remains['transit_box'] != ''),
    #                           remains['date_arrival'] + " (" + remains['transit_box'] + ")", '')

    remains = pd.pivot_table(remains, index=['code_continent',
                                             'code_nestle',
                                             'nomenclature'],
                             columns=['city'],
                             values=['free_remain', 'reserve', 'date_arrival', 'transit_box'],
                             aggfunc={'free_remain': min, 'reserve': min, 'date_arrival': min, 'transit_box': min})
    remains = remains.swaplevel(0, 1, axis=1
                                ).sort_index(axis=1, level=0, ascending=False
                                             ).reset_index().fillna('')
    # ).rename({'code_continent': 'Код',
    #           'code_nestle': 'Артикул',
    #           'nomenclature': 'Номенклатура',
    #           'free_remain': '1_Остаток',
    #           'reserve': '2_Резерв',
    #           'date_arrival': '3_Приход',
    #           'transit_box': '4_Короба'
    #           }, axis=1).fillna('')

    remains.columns.names = [None, None]

    return remains
