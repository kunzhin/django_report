from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='/')
def index(request):
    context = {'title': 'Расчет ЗП'}

    return render(request, template_name='payroll/index.html', context=context)
