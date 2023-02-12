import pandas as pd
import numpy as np


def photostream_status_df(queryset):
    df = pd.DataFrame(queryset)

    df_dsm = pd.pivot_table(df, index=['dsm__dsm'],
                            columns=['category__name'],
                            values=['status_worked_out'],
                            aggfunc={'status_worked_out': 'count'},
                            margins=True,
                            margins_name='Итого')

    df_dsm = df_dsm.swaplevel(0, 1, axis=1
                              ).droplevel(1, axis=1
                                          ).reset_index().fillna('нет фото'
                                                                 ).rename({'dsm__dsm': 'Территория'}, axis=1)
    df_dsm.columns.name = None

    df_tsm = pd.pivot_table(df, index=['tsm__tsm', 'created_at'],
                            columns=['category__name'],
                            values=['status_worked_out'],
                            aggfunc={'status_worked_out': [np.sum, 'count']},
                            fill_value=0)

    df_tsm = df_tsm.swaplevel(1, 2, axis=1
                              ).sort_values(by=['category__name'], axis=1
                                            ).droplevel(0, axis=1
                                                        ).sort_values(by=['created_at']
                                                                      ).reset_index(
    ).rename({'count': 'Аудиты',
              'sum': 'Зачёт',
              'tsm__tsm': 'Территория',
              'created_at': 'Дата'}, axis=1)

    # print(df_tsm.columns)
    #                          ).droplevel(1, axis=1
    #                                      ).reset_index().fillna('нет фото'
    #                                                             ).rename({'tsm__tsm': 'Территория'}, axis=1)
    df_tsm.columns.names = [None, None]

    return [df_dsm, df_tsm]


def data_statistics_df(queryset):
    df = pd.DataFrame(queryset)

    category_df = df.groupby(['category__name']
                             ).agg({'status_worked_out': [np.sum, 'count']}
                                   ).droplevel(0, axis=1).reset_index().rename({'category__name': 'Категория',
                                                                                'sum': 'Зачтено',
                                                                                'count': 'Аудиты'}, axis=1)

    category_df['%'] = round((category_df['Зачтено'] / category_df['Аудиты']) * 100, 0
                             ).replace(np.nan, 0
                                       ).replace(np.inf, 100)

    category_df['%'] = category_df['%'].apply(lambda x: '{0:.0f}%'.format(x))
    category_df = category_df[['Категория', 'Аудиты', 'Зачтено', '%']]

    date_df = df.groupby(['created_at']
                         ).agg({'status_worked_out': [np.sum, 'count']}
                               ).droplevel(0, axis=1).reset_index().rename({'created_at': 'Дата',
                                                                            'sum': 'Зачтено',
                                                                            'count': 'Аудиты'}, axis=1)
    date_df['%'] = round((date_df['Зачтено'] / date_df['Аудиты']) * 100, 0
                         ).replace(np.nan, 0
                                   ).replace(np.inf, 100)

    date_df['%'] = date_df['%'].apply(lambda x: '{0:.0f}%'.format(x))
    date_df = date_df[['Дата', 'Аудиты', 'Зачтено', '%']]

    # print(category_df)

    return [category_df, date_df]
