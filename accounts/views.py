from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from .update_tt import update_tt_address, hierarchy
from datetime import datetime

# Create your views here.


@user_passes_test(lambda u: u.is_superuser)
def update_hierarchy(request):
    time = hierarchy()
    return HttpResponse('Данные обновлены! Время: ' + str(time))


# Доступ только для администратора. Добавить возврат ошибок.
@user_passes_test(lambda u: u.is_superuser)
def update_tt(request):
    time = update_tt_address()
    return HttpResponse('Данные обновлены! Время: ' + str(time))
