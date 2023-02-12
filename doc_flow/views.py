from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect

from doc_flow.forms import DocumentForm
from indicators.func import df_to_html
import pandas as pd
import numpy as np
import re


@login_required(login_url='/')
def doc_flow(request):
    def invoice(df):
        result = df.drop(['typeDoc', '_merge'], axis=1).rename({'date': 'Дата',
                                                                'docNumber': 'Номер документа',
                                                                'client': 'Контрагент',
                                                                'reason': 'Причина',
                                                                'comment': 'Комментарий',
                                                                'address': 'Адрес',
                                                                'district': 'Район'
                                                                }, axis=1)
        result = result.sort_values(by=['Район', 'Дата'])

        return result[['Район', 'Дата', 'Номер документа', 'Контрагент', 'Адрес', 'Причина', 'Комментарий']]

    def withdrawn(df):
        result = df.drop(['typeDoc', '_merge', 'district', 'reason'], axis=1).rename({'date': 'Дата',
                                                                                      'docNumber': 'Номер документа',
                                                                                      'client': 'Контрагент',
                                                                                      'address': 'Адрес',
                                                                                      'comment': 'Комментарий',
                                                                                      }, axis=1)
        result = result.sort_values(by=['Комментарий'], ascending=False)

        return result[['Дата', 'Номер документа', 'Контрагент', 'Адрес', 'Комментарий']]

    def rec_report(df):
        result = df.drop(['typeDoc', '_merge', 'district', 'address'], axis=1).rename({'date': 'Дата',
                                                                                       'docNumber': 'Номер документа',
                                                                                       'client': 'Контрагент',
                                                                                       'reason': 'Причина',
                                                                                       'comment': 'Комментарий',
                                                                                       }, axis=1)
        result = result.sort_values(by=['Дата'])

        return result[['Дата', 'Номер документа', 'Контрагент', 'Причина', 'Комментарий']]

    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            xl_file1 = request.FILES['xlsxfile_1']
            xl_file2 = request.FILES['xlsxfile_2']

            try:
                data_1 = pd.read_excel(xl_file1)
                data_2 = pd.read_excel(xl_file2)
            except ValueError:
                form = DocumentForm()
                context = {
                    'title': 'Документооборот',
                    'form': form,
                    'error': 'Не корректный формат файла, выбери Excel файл с долгами по документам!'
                }

                return render(request, template_name='doc_flow/index.html', context=context)

            data = [data_1, data_2]

            res_list = []

            try:
                for item in data:
                    df = item[['Unnamed: 0', 'Unnamed: 2', 'Unnamed: 6', 'Unnamed: 9', 'Unnamed: 12', 'Unnamed: 15',
                               'Unnamed: 16']].dropna(subset=['Unnamed: 2'])

                    df_res = df[
                        df['Unnamed: 2'].str.contains('04/|И-0|Н-0|Н-В', flags=re.IGNORECASE, regex=True)].reset_index(
                        drop=True)  # Фильтруем фактуры, сверки, возвраты, гарантийные письма, реестры чеков

                    df_res = df_res.drop(np.where(
                        df_res['Unnamed: 2'].str.contains('Н-0', flags=re.IGNORECASE, regex=True) & (
                                pd.isna(df_res['Unnamed: 9']) | pd.isna(df_res['Unnamed: 6'])))[
                                             0])  # Убираем гарантийные письма, реестры чеков

                    df_res = df_res.drop_duplicates(subset='Unnamed: 2')

                    df_res = df_res.rename({
                        'Unnamed: 0': 'date',
                        'Unnamed: 2': 'docNumber',
                        'Unnamed: 6': 'client',
                        'Unnamed: 9': 'reason',
                        'Unnamed: 12': 'comment',
                        'Unnamed: 15': 'address',
                        'Unnamed: 16': 'district'
                    }, axis=1).fillna('')

                    #df_res['date'] = pd.to_datetime(df_res['date'], infer_datetime_format=True)
                    #df_res['date'] = df_res['date'].dt.strftime('%d-%m-%Y')

                    df_res['typeDoc'] = np.where(df_res['docNumber'].str.contains('04/', regex=True), 'Фактура', '')

                    df_res['typeDoc'] = np.where(df_res['docNumber'].str.contains('Н-0', regex=True), 'Акт Сверки',
                                                 df_res['typeDoc'])

                    df_res['typeDoc'] = np.where(df_res['docNumber'].str.contains('Н-В', regex=True), 'Возврат',
                                                 df_res['typeDoc'])

                    df_res['typeDoc'] = np.where(df_res['docNumber'].str.contains('И-0', regex=True), 'Реклама',
                                                 df_res['typeDoc'])

                    res_list.append(df_res)

            except KeyError:
                form = DocumentForm()
                context = {
                    'title': 'Документооборот',
                    'form': form,
                    'error': 'Не корректный файл долгов, выбери Excel файл с долгами по документам!'
                }
                return render(request, template_name='doc_flow/index.html', context=context)

            dataframe = res_list[1].merge(res_list[0],
                                          on=['date', 'docNumber', 'client', 'reason', 'comment', 'address',
                                              'district', 'typeDoc'], indicator=True, how='outer')

            rem_invoice = dataframe.loc[(dataframe['_merge'] == 'right_only') & (dataframe['typeDoc'] == 'Фактура')]
            rem_withdrawn = dataframe.loc[(dataframe['_merge'] == 'right_only') & (dataframe['typeDoc'] == 'Возврат')]
            rem_as = dataframe.loc[(dataframe['_merge'] == 'right_only') & (dataframe['typeDoc'] == 'Акт Сверки')]

            is_invoice = dataframe.loc[(dataframe['_merge'] == 'left_only') & (dataframe['typeDoc'] == 'Фактура')]
            is_withdrawn = dataframe.loc[(dataframe['_merge'] == 'left_only') & (dataframe['typeDoc'] == 'Возврат')]
            is_as = dataframe.loc[(dataframe['_merge'] == 'left_only') & (dataframe['typeDoc'] == 'Акт Сверки')]

            debt_invoice = dataframe.loc[
                (dataframe['_merge'].isin(['both', 'left_only'])) & (dataframe['typeDoc'] == 'Фактура')]
            debt_withdrawn = dataframe.loc[
                (dataframe['_merge'].isin(['both', 'left_only'])) & (dataframe['typeDoc'] == 'Возврат')]
            debt_as = dataframe.loc[
                (dataframe['_merge'].isin(['both', 'left_only'])) & (dataframe['typeDoc'] == 'Акт Сверки')]

            context = {'title': 'Документооборот',
                       'form': form,

                       'rem_invoice_count': len(rem_invoice),
                       'rem_invoice': df_to_html(invoice(rem_invoice), 'rem_invoce'),

                       'rem_withdrawn_count': len(rem_withdrawn),
                       'rem_withdrawn': df_to_html(withdrawn(rem_withdrawn), 'rem_withdrawn'),

                       'rem_as_count': len(rem_as),
                       'rem_as': df_to_html(rec_report(rem_as), 'rem_as'),

                       'is_invoice_count': len(is_invoice),
                       'is_invoice': df_to_html(invoice(is_invoice), 'is_invoice'),

                       'is_withdrawn_count': len(is_withdrawn),
                       'is_withdrawn': df_to_html(withdrawn(is_withdrawn), 'is_withdrawn'),

                       'is_as_count': len(is_as),
                       'is_as': df_to_html(rec_report(is_as), 'is_as'),

                       'debt_invoice_count': len(debt_invoice),
                       'debt_invoice': df_to_html(invoice(debt_invoice), 'debt_invoice'),

                       'debt_withdrawn_count': len(debt_withdrawn),
                       'debt_withdrawn': df_to_html(withdrawn(debt_withdrawn), 'debt_withdrawn'),

                       'debt_as_count': len(debt_as),
                       'debt_as': df_to_html(rec_report(debt_as), 'debt_as'),
                       }

        return render(request, template_name='doc_flow/result.html', context=context)
    else:
        form = DocumentForm()  # A empty, unbound form

        context = {
            'title': 'Документооборот',
            'form': form,
        }

        return render(request, template_name='doc_flow/index.html', context=context)
