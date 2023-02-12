from fileinput import filename
from django.db import models
from django.dispatch.dispatcher import receiver
from django.db.models.signals import pre_delete
from django import forms
import os
from functools import partial


# Create your models here.


class Remains(models.Model):
    code_category = models.CharField(max_length=3, verbose_name='Код категории', db_column='Код категории')
    category = models.CharField(max_length=255, verbose_name='Категория', db_column='Категория')
    code_continent = models.CharField(max_length=5, verbose_name='Код', db_column='Код')
    code_nestle = models.CharField(max_length=8, verbose_name='Артикул', db_column='Артикул')
    nomenclature = models.CharField(max_length=255, verbose_name='Номенклатура', db_column='Номенклатура')
    remaining = models.IntegerField(verbose_name='Остаток', db_column='Остаток', blank=True)
    reserve = models.BigIntegerField(verbose_name='Резерв', db_column='Резерв', blank=True)
    free_remain = models.IntegerField(verbose_name='Свободный остаток', db_column='Свободный остаток', blank=True)
    expiration_date = models.DateField(verbose_name='Срок годности', db_column='Срок годности', blank=True)
    remaining_term = models.CharField(max_length=5, verbose_name='Остаток срока', db_column='Остаток срока', blank=True)
    date_arrival = models.DateField(verbose_name='Дата прихода', db_column='Дата прихода', blank=True)
    transit_box = models.IntegerField(verbose_name='Транзит (Короб)', db_column='Транзит (Короб)', blank=True)
    city = models.CharField(max_length=50, verbose_name='Город', db_column='Город')
    topx = models.CharField(max_length=255, verbose_name='TOPX', db_column='TOPX')
    status = models.CharField(max_length=255, verbose_name='Статус позиции', db_column='status')
    launch = models.CharField(max_length=255, verbose_name='Новая позиция', db_column='launch')

    def __str__(self):
        return self.nomenclature

    class Meta:
        verbose_name = 'Остатки'
        verbose_name_plural = 'Остатки'
        ordering = ['code_category', '-nomenclature']


class CategoryRemains(models.Model):
    code_category = models.CharField(max_length=3, verbose_name='Код категории', db_column='Код категории')
    category = models.CharField(max_length=255, verbose_name='Категория', db_column='Категория')

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Категория остатков'
        verbose_name_plural = 'Категории остатков'
        ordering = ['code_category']


class Suspended(models.Model):
    dbc = models.CharField(max_length=255, verbose_name='DBC', db_column='DBC')
    code_nestle = models.IntegerField(verbose_name='Код товара', db_column='код товара')
    status = models.CharField(max_length=255, verbose_name='Статус позиции', db_column='status')

    def __str__(self):
        return self.dbc

    class Meta:
        verbose_name = 'Позиция на вывод'
        verbose_name_plural = 'Позиции на вывод'


class Launch(models.Model):
    dbc = models.CharField(max_length=255, verbose_name='DBC', db_column='DBC')
    code_nestle = models.IntegerField(verbose_name='Код товара', db_column='код товара')
    dbc_name = models.CharField(max_length=255, verbose_name='Наименование DBC', db_column='наименование DBC')
    launch = models.CharField(max_length=255, verbose_name='Новая позиция', db_column='launch')

    def __str__(self):
        return self.dbc_name

    class Meta:
        verbose_name = 'Позиция на запуск'
        verbose_name_plural = 'Позиции на запуски'


# Функция переименования загружаемого файла
def _update_filename(instance, filename, path, place, file):
    path = path

    ext = filename.split('.')[-1]

    filename = '{}_{}.{}'.format(file, place, ext)

    return os.path.join(path, place, filename)


def upload_to(path, place, file):
    return partial(_update_filename, path=path, place=place, file=file)


class RemainsFile(models.Model):
    date = models.DateField(verbose_name='Дата загрузки', auto_now=True)

    nkz = models.FileField(verbose_name='Главный склад Новокузнецк',
                           upload_to=upload_to('remains', 'nkz', 'remains'),
                           blank=True)
    nkz_transit = models.FileField(verbose_name='Транзиты Новокузнецк',
                                   upload_to=upload_to('remains', 'nkz', 'transit'),
                                   blank=True)
    nkz_expiration = models.FileField(verbose_name='Сроки Новокузнецк',
                                      upload_to=upload_to('remains', 'nkz', 'expiration'),
                                      blank=True)

    nsk = models.FileField(verbose_name='Главный склад Новосибирск',
                           upload_to=upload_to('remains', 'nsk', 'remains'),
                           blank=True)
    nsk_transit = models.FileField(verbose_name='Транзиты Новосибирск',
                                   upload_to=upload_to('remains', 'nsk', 'transit'),
                                   blank=True)
    nsk_expiration = models.FileField(verbose_name='Сроки Новосибирск',
                                      upload_to=upload_to('remains', 'nsk', 'expiration'),
                                      blank=True)

    omsk = models.FileField(verbose_name='Главный склад Омск',
                            upload_to=upload_to('remains', 'omsk', 'remains'),
                            blank=True)
    omsk_transit = models.FileField(verbose_name='Транзиты Омск',
                                    upload_to=upload_to('remains', 'omsk', 'transit'),
                                    blank=True)
    omsk_expiration = models.FileField(verbose_name='Сроки Омск',
                                       upload_to=upload_to('remains', 'omsk', 'expiration'),
                                       blank=True)

    krs = models.FileField(verbose_name='Главный склад Красноярск',
                           upload_to=upload_to('remains', 'krs', 'remains'),
                           blank=True)
    krs_transit = models.FileField(verbose_name='Транзиты Красноярск',
                                   upload_to=upload_to('remains', 'krs', 'transit'),
                                   blank=True)
    krs_expiration = models.FileField(verbose_name='Сроки Красноярск',
                                      upload_to=upload_to('remains', 'krs', 'expiration'),
                                      blank=True)

    abk = models.FileField(verbose_name='Главный склад Абакан',
                           upload_to=upload_to('remains', 'abk', 'remains'),
                           blank=True)
    abk_transit = models.FileField(verbose_name='Транзиты Абакан',
                                   upload_to=upload_to('remains', 'abk', 'transit'),
                                   blank=True)
    abk_expiration = models.FileField(verbose_name='Сроки Абакан',
                                      upload_to=upload_to('remains', 'abk', 'expiration'),
                                      blank=True)

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = 'Загрузка остатков'
        verbose_name_plural = 'Загрузка остатков'


@receiver(pre_delete, sender=RemainsFile)
def file_model_delete(sender, instance, **kwargs):
    if instance.nkz.name:
        instance.nkz.delete(False)
    if instance.nsk.name:
        instance.nsk.delete(False)
    if instance.omsk.name:
        instance.omsk.delete(False)
    if instance.krs.name:
        instance.krs.delete(False)
    if instance.abk.name:
        instance.abk.delete(False)

    if instance.nkz_transit.name:
        instance.nkz_transit.delete(False)
    if instance.nsk_transit.name:
        instance.nsk_transit.delete(False)
    if instance.omsk_transit.name:
        instance.omsk_transit.delete(False)
    if instance.krs_transit.name:
        instance.krs_transit.delete(False)
    if instance.abk_transit.name:
        instance.abk_transit.delete(False)

    if instance.nkz_expiration.name:
        instance.nkz_expiration.delete(False)
    if instance.nsk_expiration.name:
        instance.nsk_expiration.delete(False)
    if instance.omsk_expiration.name:
        instance.omsk_expiration.delete(False)
    if instance.krs_expiration.name:
        instance.krs_expiration.delete(False)
    if instance.abk_expiration.name:
        instance.abk_expiration.delete(False)
