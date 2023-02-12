from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

# Create your models here.


class VolumePlanESR(models.Model):
    esr = models.CharField(max_length=255, verbose_name='ESR', db_column='ESR')
    tier = models.CharField(max_length=255, verbose_name='Tier', db_column='Tier')
    rev_pre_group = models.CharField(max_length=255, verbose_name='Подгруппа ревизии', db_column='RevPreGroup')
    rev_group = models.CharField(max_length=255, verbose_name='Группа ревизии', db_column='Revision Group')
    target = models.IntegerField(verbose_name='План(руб.)', db_column='Target')


class VolumePlanTSM(models.Model):
    dsm = models.CharField(max_length=255, verbose_name='DSM', db_column='DSM')
    tsm = models.CharField(max_length=255, verbose_name='TSM', db_column='TSM')
    tier = models.CharField(max_length=255, verbose_name='Tier', db_column='Tier')
    rev_pre_group = models.CharField(max_length=255, verbose_name='Подгруппа ревизии', db_column='RevPreGroup')
    target = models.IntegerField(verbose_name='План(руб.)', db_column='Target')
    rev_group = models.CharField(max_length=255, verbose_name='Группа ревизии', db_column='Revision Group')


class TopPlan(models.Model):
    category = models.CharField(max_length=255, verbose_name='Категория', db_column='Категория')
    dbc = models.CharField(max_length=255, verbose_name='DBC', db_column='DBC')
    dbc_name = models.CharField(max_length=255, verbose_name='Наименование DBC', db_column='наименование DBC')
    esr = models.CharField(max_length=255, verbose_name='ESR', db_column='ESR')
    target = models.IntegerField(verbose_name='План(sku)', db_column='Target')
    dsm = models.CharField(max_length=255, verbose_name='DSM', db_column='DSM')
    tsm = models.CharField(max_length=255, verbose_name='TSM', db_column='TSM')


class CoveragePlan(models.Model):
    rsm = models.CharField(max_length=255, verbose_name='RSM', db_column='RSM')
    esr = models.CharField(max_length=255, verbose_name='ESR', db_column='ESR')
    target = models.IntegerField(verbose_name='План(ТТ)', db_column='Target')
    dsm = models.CharField(max_length=255, verbose_name='DSM', db_column='DSM')
    tsm = models.CharField(max_length=255, verbose_name='TSM', db_column='TSM')


class DistrTaskPlan(models.Model):
    esr = models.CharField(max_length=255, verbose_name='ESR', db_column='ESR')
    distr_task = models.CharField(max_length=255, verbose_name='Задача', db_column="distr_task")
    target = models.IntegerField(verbose_name='План(ТТ)', db_column='Target')
    rsm = models.CharField(max_length=255, verbose_name='RSM', db_column='RSM')
    dsm = models.CharField(max_length=255, verbose_name='DSM', db_column='DSM')
    tsm = models.CharField(max_length=255, verbose_name='TSM', db_column='TSM')

    def __str__(self):
        return self.distr_task

    class Meta:
        verbose_name = 'План по задаче Усиления'
        verbose_name_plural = 'Планы по задачам Усиления'
        ordering = ['distr_task']


class I2lTaskPlan(models.Model):
    esr = models.CharField(max_length=255, verbose_name='ESR', db_column='ESR')
    distr_task = models.CharField(max_length=255, verbose_name='Задача', db_column="distr_task")
    view_task = models.CharField(max_length=255, verbose_name='Вид задачи', db_column='view_task')
    target = models.IntegerField(verbose_name='План', db_column='Target')
    rsm = models.CharField(max_length=255, verbose_name='RSM', db_column='RSM')
    dsm = models.CharField(max_length=255, verbose_name='DSM', db_column='DSM')
    tsm = models.CharField(max_length=255, verbose_name='TSM', db_column='TSM')

    def __str__(self):
        return self.distr_task

    class Meta:
        verbose_name = 'План по дистрибуционной задаче'
        verbose_name_plural = 'Планы по дистрибуционным задачам'
        ordering = ['distr_task']


class VolumeCategory(models.Model):
    group = models.CharField(max_length=255, verbose_name='Группа', db_column='группа')
    rev_pre_group = models.CharField(max_length=255, verbose_name='Подгруппа ревизии', db_column='RevPreGroup')
    rev_group = models.CharField(max_length=255, verbose_name='Группа ревизии', db_column='Revision Group')

    def __str__(self):
        return self.group

    class Meta:
        verbose_name = 'Категория объема'
        verbose_name_plural = 'Категории объема'
        ordering = ['group']


class TopCategory(models.Model):
    dbc = models.CharField(max_length=10, verbose_name='DBC', db_column='DBC')
    rev_group_top = models.CharField(max_length=255, verbose_name='Группа ревизии ТопХ', db_column='RevGroupTopX')
    min_sell = models.IntegerField(verbose_name='Порог зачета', db_column='Min_sell')
    dbc_name = models.CharField(max_length=255, verbose_name='Наименование DBC', db_column='наименование DBC')

    def __str__(self):
        return self.dbc_name

    class Meta:
        verbose_name = 'Категория ТопХ'
        verbose_name_plural = 'Категории ТопХ'
        ordering = ['rev_group_top']


class TaskCategory(models.Model):
    dbc_name = models.CharField(max_length=255, verbose_name='Наименование DBC', db_column='наименование DBC')
    distr_task = models.CharField(max_length=255, verbose_name='Задача', db_column="distr_task")

    def __str__(self):
        return self.dbc_name

    class Meta:
        verbose_name = 'Задача по SKU'
        verbose_name_plural = 'Задачи по SKU'


class Report07(models.Model):
    region = models.CharField(max_length=255, verbose_name='Площадка', db_column='Площадка')
    rsm = models.CharField(max_length=255, verbose_name='RSM', db_column='RSM', db_index=True)
    dsm = models.CharField(max_length=255, verbose_name='DSM', db_column='DSM', db_index=True)
    tsm = models.CharField(max_length=255, verbose_name='TSM', db_column='TSM', db_index=True)
    esr = models.CharField(max_length=255, verbose_name='ESR', db_column='ESR', db_index=True)
    tier = models.CharField(max_length=255, verbose_name='Tier', db_column='Tier', db_index=True)
    stream_tk = models.CharField(max_length=255, verbose_name='Стрим ТК', db_column='Стрим ТК')
    virtual = models.CharField(max_length=255, verbose_name='Виртуальность', db_column='виртуальность')
    code_tt_kis = models.CharField(max_length=255, verbose_name='Код ТТ КИС', db_column='код ТТ КИС')
    code_tt = models.CharField(max_length=255, verbose_name='код ТТ', db_column='код ТТ')
    name_tt = models.CharField(max_length=255, verbose_name='Наименование ТТ', db_column='наименование ТТ', db_index=True)
    address_tt = models.CharField(max_length=255, verbose_name='Адрес ТТ', db_column='адрес ТТ', db_index=True)
    specialization_tt = models.CharField(max_length=255, verbose_name='Специализация ТТ', db_column='Специализация ТТ')
    channel_tt = models.CharField(max_length=255, verbose_name='Канал ТТ', db_column='канал ТТ', db_index=True)
    key_retail = models.CharField(max_length=255, verbose_name='Ключевая розница', db_column='Ключевая розница')
    key_whs = models.CharField(max_length=255, verbose_name='Ключевой опт', db_column='Ключевой опт')
    network = models.CharField(max_length=255, verbose_name='Сеть', db_column='сеть')
    document_number = models.CharField(max_length=255, verbose_name='Номер документа', db_column='номер документа')
    document_date = models.DateField(verbose_name='Дата документа', db_column='дата документа')
    date_shipment = models.DateField(verbose_name='Дата отгрузки', db_column='дата отгрузки', db_index=True)
    document_type = models.CharField(max_length=255, verbose_name='Тип документа', db_column='тип документа')
    month = models.IntegerField(verbose_name='Месяц', db_column='месяц')
    week = models.IntegerField(verbose_name='Неделя', db_column='Неделя')
    day = models.IntegerField(verbose_name='День', db_column='день')
    dbc = models.CharField(max_length=255, verbose_name='DBC', db_column='DBC', db_index=True)
    dbc_name = models.CharField(max_length=255, verbose_name='Наименование DBC', db_column='наименование DBC', db_index=True)
    code_nestle = models.IntegerField(verbose_name='Код товара', db_column='код товара')
    product = models.CharField(max_length=255, verbose_name='Товар', db_column='товар')
    category = models.CharField(max_length=255, verbose_name='Категория', db_column='категория')
    group = models.CharField(max_length=255, verbose_name='Группа', db_column='группа')
    pre_group = models.CharField(max_length=255, verbose_name='Подгруппа', db_column='подгруппа')
    sum_sell = models.FloatField(verbose_name='Сумма продаж', db_column='Сумма продаж (руб.)')
    sum_sell_no_nds = models.FloatField(verbose_name='Сумма продаж БЕЗ НДС', db_column='Сумма продаж БЕЗ НДС (руб.)')
    count_piece = models.IntegerField(verbose_name='Количество', db_column='Количество (шт.)')
    weight = models.FloatField(verbose_name='Вес (кг.)', db_column='Вес (кг.)')
    price = models.FloatField(verbose_name='Цена', db_column='Price')
    rev_pre_group = models.CharField(max_length=255, verbose_name='Подгруппа ревизии', db_column='RevPreGroup')
    rev_group = models.CharField(max_length=255, verbose_name='Группа ревизии', db_column='Revision Group')
    rev_group_top = models.CharField(max_length=255, verbose_name='Группа ревизии ТопХ', db_column='RevGroupTopX')
    min_sell = models.FloatField(verbose_name='Порог зачета', db_column='Min_sell')
    topx = models.CharField(max_length=255, verbose_name='Статус ТопХ', db_column='TOP')

    def __str__(self):
        return self.region

    class Meta:
        verbose_name = 'Отчет по продажам'
        verbose_name_plural = 'Отчет по продажам'
        ordering = ['region']


class Report770(models.Model):
    month = models.CharField(max_length=255, verbose_name='Месяц', db_column='Месяц')
    date_foto = models.DateField(verbose_name='Дата документа', db_column='Дата документа')
    channel_tt = models.CharField(max_length=255, verbose_name='Канал ТТ', db_column='Канал ТТ')
    network = models.CharField(max_length=255, verbose_name='Вывеска сети', db_column='Вывеска сети')
    region = models.CharField(max_length=255, verbose_name='Площадка', db_column='Площадка')
    rsm = models.CharField(max_length=255, verbose_name='RSM', db_column='RSM')
    dsm = models.CharField(max_length=255, verbose_name='DSM', db_column='DSM')
    tsm = models.CharField(max_length=255, verbose_name='TSM', db_column='TSM')
    esr = models.CharField(max_length=255, verbose_name='ESR', db_column='ESR')
    code_tt = models.CharField(max_length=255, verbose_name='Код ТТ', db_column='Код ТТ')
    name_tt = models.CharField(max_length=255, verbose_name='Название ТТ', db_column='Название ТТ')
    address_tt = models.CharField(max_length=255, verbose_name='Адрес ТТ', db_column='Адрес ТТ')
    category = models.CharField(max_length=255, verbose_name='Категория', db_column='Категория')
    status_price = models.CharField(max_length=10, verbose_name='Статус снижения цены', db_column='Статус снижения цены')
    standart_shop = models.CharField(max_length=10, verbose_name='Стандартный магазин', db_column='Стандартный магазин')
    foto_url = models.CharField(max_length=255, verbose_name='URL', db_column='URL')
    status = models.IntegerField(verbose_name='Статус', db_column='Статус')

    def __str__(self):
        return self.region

    class Meta:
        verbose_name = 'Отчет по фотопотоку'
        verbose_name_plural = 'Отчет по фотопотоку'
        ordering = ['region']

class Report770File(models.Model):
    date = models.DateField(verbose_name='Дата загрузки', auto_now=True)
    plan = models.FileField(verbose_name='Файл', upload_to='indicators/report_770', blank=False)

    class Meta:
        verbose_name = 'Загрузка 770'
        verbose_name_plural = 'Загрузка 770'

    def __str__(self):
        return str(self.date)


class Report145(models.Model):
    region = models.CharField(max_length=255, verbose_name='Площадка', db_column='Наименование площадки')
    rsm = models.CharField(max_length=255, verbose_name='RSM', db_column='RSM')
    dsm = models.CharField(max_length=255, verbose_name='DSM', db_column='DSM')
    tsm = models.CharField(max_length=255, verbose_name='TSM', db_column='TSM')
    esr = models.CharField(max_length=255, verbose_name='ESR', db_column='Имя ESR')
    code_tt = models.CharField(max_length=255, verbose_name='ID ТТ', db_column='ID ТТ')
    code_tt_kis = models.CharField(max_length=255, verbose_name='Код ТТ КИС', db_column='XCRM GUID')
    name_tt = models.CharField(max_length=255, verbose_name='Наименование ТТ', db_column='Название ТТ', blank=True)
    address_tt = models.CharField(max_length=255, verbose_name='Адрес ТТ', db_column='Адрес', blank=True)
    channel_tt = models.CharField(max_length=255, verbose_name='Канал ТТ', db_column='Канал ТТ')
    tier = models.CharField(max_length=255, verbose_name='Tier', db_column='Tier')
    category = models.CharField(max_length=255, verbose_name='Категория', db_column='Ассортимент')
    dbc = models.CharField(max_length=255, verbose_name='DBC', db_column='DBC ID', blank=True)
    dbc_name = models.CharField(max_length=255, verbose_name='Наименование DBC', db_column='Наименование DBC', blank=True)
    month = models.CharField(max_length=255, verbose_name='Месяц', db_column='Месяц')
    sum_sell = models.FloatField(verbose_name='Сумма продаж', db_column='Объем продаж точки')
    purina_except = models.CharField(max_length=255, verbose_name='Purina_except', db_column='Purina_except', blank=True, null=True)

    def __str__(self):
        return self.region

    class Meta:
        verbose_name = '145й отчет усилений'
        verbose_name_plural = '145й отчет усилений'
        ordering = ['region']


class ReportFile(models.Model):
    date = models.DateField(verbose_name='Дата загрузки', auto_now=True)

    nkz_07 = models.FileField(verbose_name='Новокузнецк_07', upload_to='indicators/report07', blank=True)
    nsk_07 = models.FileField(verbose_name='Новосибирск_07', upload_to='indicators/report07', blank=True)
    omsk_07 = models.FileField(verbose_name='Омск_07', upload_to='indicators/report07', blank=True)
    krs_07 = models.FileField(verbose_name='Красноярск_07', upload_to='indicators/report07', blank=True)
    abk_07 = models.FileField(verbose_name='Абакан_07', upload_to='indicators/report07', blank=True)

    nkz_145 = models.FileField(verbose_name='Новокузнецк_145', upload_to='indicators/report145', blank=True)
    nsk_145 = models.FileField(verbose_name='Новосибирск_145', upload_to='indicators/report145', blank=True)
    omsk_145 = models.FileField(verbose_name='Омск_145', upload_to='indicators/report145', blank=True)
    krs_145 = models.FileField(verbose_name='Красноярск_145', upload_to='indicators/report145', blank=True)
    abk_145 = models.FileField(verbose_name='Абакан_145', upload_to='indicators/report145', blank=True)

    class Meta:
        verbose_name = 'Загрузка 07 и 145'
        verbose_name_plural = 'Загрузка 07 и 145'

    def __str__(self):
        return str(self.date)


class PlanFile(models.Model):
    date = models.DateField(verbose_name='Дата загрузки', auto_now=True)
    plan = models.FileField(verbose_name='Файл', upload_to='indicators/xls_plan', blank=False)

    class Meta:
        verbose_name = 'Загрузка плана'
        verbose_name_plural = 'Загрузка планов'

    def __str__(self):
        return str(self.date)


class Month(models.Model):
    """Модель хранящая Месяца"""
    month = models.CharField(max_length=255, verbose_name='Месяц')

    def __str__(self):
        return self.month

    class Meta:
        verbose_name_plural = 'Месяца'
        verbose_name = 'Месяц'


class Tier(models.Model):
    """Модель хранящая Tier TT"""
    tier = models.CharField(max_length=255, verbose_name='Tier', db_column='Tier')

    def __str__(self):
        return self.tier

    class Meta:
        verbose_name_plural = 'Tier'
        verbose_name = 'Tier'


class ChannelTT(models.Model):
    """Модель хранящая канылы ТТ"""
    channel = models.CharField(max_length=255, verbose_name='Канал ТТ', db_column='канал ТТ')

    def __str__(self):
        return self.channel

    class Meta:
        verbose_name_plural = 'Каналы ТТ'
        verbose_name = 'Канал ТТ'


class DBCName(models.Model):
    """Модель хранящая наименования DBC"""
    DBC_name = models.CharField(max_length=255, unique=True, verbose_name='Наименование DBC', db_column='наименование DBC')

    def __str__(self):
        return self.DBC_name

    class Meta:
        verbose_name_plural = 'Наименования DBC запусков'
        verbose_name = 'Наименование DBC запуска'


class IdeaToLaunch(models.Model):
    COUNT_METHOD = [
        ('sum_dbc', 'Сумма кол-ва всех SKU (3шт + 3шт)'),
        ('count_dbc', 'Сумма проданных DBC в ТТ (1sku + 1sku +... от 2шт'),
        ('count_sum_dbc', 'Сумма обязательных DBC (2sku по 8шт)'),
    ]

    '''Список задач из планов'''
    task_list = I2lTaskPlan.objects.all().values_list('distr_task', 'distr_task').distinct()

    '''Модель запусков'''
    task_name = models.CharField(max_length=255, verbose_name='Задача', db_column='task', choices=task_list)
    description = models.TextField(verbose_name='Описание', db_column='description', default='')
    dbc = models.ManyToManyField('DBCName', verbose_name='Участвующие позиции')
    min_threshold = models.IntegerField(verbose_name='Минимальный порог зачёта', db_column='min_threshold', default=0)
    # months = models.ManyToManyField('Month', verbose_name='Период')
    tier = models.ManyToManyField('Tier', verbose_name='Tier')
    channel = models.ManyToManyField('ChannelTT', verbose_name='Каналы ТТ')
    func_launch = models.CharField(max_length=255, verbose_name='Метод подсчета', choices=COUNT_METHOD)
    info_tt_view = models.BooleanField(verbose_name='Показ в продажах по ТТ', default=False)
    day_start = models.DateField(verbose_name='Дата начала', db_column='day_start')
    day_end = models.DateField(verbose_name='Дата окончания', db_column='day_end')

    def __str__(self):
        return self.task_name

    '''Список месяцев'''
    def month_list(self):
        return [self.day_start, self.day_end]

    month_list.short_description = 'Период зачета'

    '''Список наименований DBC'''
    def dbc_list(self):
        return list(self.dbc.values_list('DBC_name', flat=True))

    dbc_list.short_description = 'Наименования DBC'

    '''Список Tier'''
    def tier_list(self):
        return list(self.tier.values_list('tier', flat=True))

    tier_list.short_description = 'Tier'

    '''Список каналов'''
    def channel_list(self):
        return list(self.channel.values_list('channel', flat=True))

    channel_list.short_description = 'Каналы ТТ'

    class Meta:
        verbose_name_plural = 'Запуски'
        verbose_name = 'Запуск'
        ordering = ['task_name']


class ClientException(models.Model):
    code_tt = models.CharField(max_length=255, verbose_name='Код ТТ', db_column='code_tt')
    status = models.CharField(max_length=255, verbose_name='Статус', db_column='status')

    class Meta:
        verbose_name_plural = 'Исключения'
        verbose_name = 'Исключение'


@receiver(pre_delete, sender=ReportFile)
def file_model_delete(sender, instance, **kwargs):
    if instance.nkz_07.name:
        instance.nkz_07.delete(False)
    if instance.nsk_07.name:
        instance.nsk_07.delete(False)
    if instance.omsk_07.name:
        instance.omsk_07.delete(False)
    if instance.krs_07.name:
        instance.krs_07.delete(False)
    if instance.abk_07.name:
        instance.abk_07.delete(False)

    if instance.nkz_145.name:
        instance.nkz_145.delete(False)
    if instance.nsk_145.name:
        instance.nsk_145.delete(False)
    if instance.omsk_145.name:
        instance.omsk_145.delete(False)
    if instance.krs_145.name:
        instance.krs_145.delete(False)
    if instance.abk_145.name:
        instance.abk_145.delete(False)


@receiver(pre_delete, sender=PlanFile)
def file_model_delete(sender, instance, **kwargs):
    if instance.plan.name:
        instance.plan.delete(False)


@receiver(pre_delete, sender=Report770File)
def file_model_delete(sender, instance, **kwargs):
    if instance.plan.name:
        instance.plan.delete(False)











