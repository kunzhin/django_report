from django import forms


class DocumentForm(forms.Form):
    xlsxfile_1 = forms.FileField(
        label='Выбери файл долгов по документам от первого числа текущего месяца',
        help_text='max. 42 megabytes',
    )

    xlsxfile_2 = forms.FileField(
        label='Выбери файл долгов по документам на текущий момент',
        help_text='max. 42 megabytes',
    )
