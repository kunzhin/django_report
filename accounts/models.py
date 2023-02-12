from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class DSM(models.Model):
    dsm = models.CharField(max_length=255, verbose_name='Территория DSM', db_column='DSM')

    def __str__(self) -> str:
        return self.dsm

    class Meta:
        verbose_name = 'Территория DSM'
        verbose_name_plural = 'Территории DSM'


class TSM(models.Model):
    tsm = models.CharField(max_length=255, verbose_name='Территория TSM', db_column='TSM')
    dsm = models.ForeignKey(DSM, on_delete=models.PROTECT, null=False, verbose_name='Территория DSM')

    def __str__(self) -> str:
        return self.tsm

    class Meta:
        verbose_name = 'Территория TSM'
        verbose_name_plural = 'Территории TSM'
        ordering = ['dsm']


class ESR(models.Model):
    esr = models.CharField(max_length=255, verbose_name='Территория ESR', db_column='ESR')
    tsm = models.ForeignKey(TSM, on_delete=models.PROTECT, null=False, verbose_name='Территория TSM')

    def __str__(self) -> str:
        return self.esr

    class Meta:
        verbose_name = 'Территория ESR'
        verbose_name_plural = 'Территории ESR'
        ordering = ['tsm']


class TT(models.Model):
    tt = models.CharField(max_length=255, verbose_name='Наименование ТТ', db_column='наименование ТТ')
    esr = models.ForeignKey(ESR, on_delete=models.CASCADE, null=False, verbose_name='Территория ESR')

    def __str__(self) -> str:
        return self.tt

    class Meta:
        verbose_name = 'Наименование ТТ'
        verbose_name_plural = 'Наименования ТТ'
        ordering = ['esr']


class Address(models.Model):
    code_tt = models.CharField(max_length=255, verbose_name='код ТТ', db_column='код ТТ')
    kis_code = models.CharField(max_length=255, verbose_name='Код ТТ КИС', db_column='код ТТ КИС')
    tier = models.CharField(max_length=255, verbose_name='Tier', db_column='Tier')
    channel_tt = models.CharField(max_length=255, verbose_name='Канал ТТ', db_column='канал ТТ')
    address = models.CharField(max_length=255, verbose_name='Адрес ТТ', db_column='адрес ТТ')
    tt = models.ForeignKey(TT, on_delete=models.CASCADE, null=False, verbose_name='Наименование ТТ')
    day_route = models.CharField(max_length=255, verbose_name='День недели', db_column='day_route')

    def __str__(self) -> str:
        return self.address

    class Meta:
        verbose_name = 'Адрес ТТ'
        verbose_name_plural = 'Адреса ТТ'
        ordering = ['tt']


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, null=False)
    avatar = models.ImageField(upload_to='avatar/users', verbose_name='Аватар', blank=True)
    dsm = models.ForeignKey(DSM, on_delete=models.PROTECT, null=True, verbose_name='Территория DSM')
    tsm = models.ForeignKey(TSM, on_delete=models.PROTECT, verbose_name='Территория TSM', blank=True, null=True)
    esr = models.ForeignKey(ESR, on_delete=models.PROTECT, verbose_name='Территория ESR', blank=True, null=True)

    def __unicode__(self):
        return self.user

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Hierarchy(models.Model):
    rsm = models.CharField(max_length=255, verbose_name='Территория RSM', db_column='RSM')
    dsm = models.CharField(max_length=255, verbose_name='Территория DSM', db_column='DSM')
    tsm = models.CharField(max_length=255, verbose_name='Территория TSM', db_column='TSM')
    esr = models.CharField(max_length=255, verbose_name='Территория ESR', db_column='ESR')

    def __unicode__(self):
        return self.esr

    class Meta:
        verbose_name = 'Иерархия'
        verbose_name_plural = 'Иерархия'
        ordering = ['dsm', 'tsm', 'esr']
