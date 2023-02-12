from django.db import models
from django.db.models.base import Model
from django.urls import reverse
import requests
import json
from accounts.models import DSM, TSM, ESR, TT, Address

# Create your models here.


class CategoryPhoto(models.Model):
    name = models.CharField(max_length=255, verbose_name='Категория фото')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Категория фото'
        verbose_name_plural = 'Категории фото'


class PhotostreamForm(models.Model):
    dsm = models.ForeignKey(DSM, on_delete=models.PROTECT, null=False, verbose_name='Территория DSM')
    tsm = models.ForeignKey(TSM, on_delete=models.PROTECT, null=False, verbose_name='Территория TSM')
    esr = models.ForeignKey(ESR, on_delete=models.PROTECT, null=False, verbose_name='Территория ESR')
    tt = models.CharField(max_length=255, null=False, verbose_name='Наименование ТТ')
    address = models.CharField(max_length=255, null=False, verbose_name='Адрес ТТ')
    category = models.ForeignKey(CategoryPhoto, on_delete=models.PROTECT, null=False, verbose_name='Категория фото')
    url_photo = models.URLField(max_length=255, verbose_name='Ссылка на фото', unique=True)
    photo = models.ImageField(blank=True, upload_to='photos/%Y/%m/%d', verbose_name='Фото')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата оценки фото')
    status_worked_out = models.BooleanField(default=False, verbose_name='Зачёт (Да/Нет)')
    date_correction = models.DateField(blank=True, null=True, verbose_name='Дата исправления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    # Получаем абсолютною ссылку на запись модели
    def get_absolute_url(self):
        return reverse("view_photostream_audit", kwargs={"pk": self.pk})

    # Обрабатываем ссылку на фото перед записью в базу, получаем прямую сслыку на фото
    def get_image_url(self):
        img_url = self.url_photo
        img_url_split = img_url.split('/')
        if 'stamped_file' in img_url:
            self.url_photo = img_url
        else:
            url = 'https://photo.nestle.ru/api/public/v1/photos/' + img_url_split[-1]
            response = requests.get(url)
            image_url = json.loads(response.text)['stamped_file']
            self.url_photo = image_url

    def get_tsm_dsm(self):
        esr = ESR.objects.get(esr=self.esr)
        tsm = TSM.objects.get(tsm=esr.tsm)
        self.tsm = esr.tsm
        self.dsm = tsm.dsm

    # Переопределенный метод save() для сохранения прямой ссылки в модель
    def save(self, *args, **kwargs):
        self.get_image_url()
        self.get_tsm_dsm()
        super(PhotostreamForm, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.tt

    class Meta:
        verbose_name = 'Фотопоток'
        verbose_name_plural = 'Фотопоток'
        ordering = ['-created_at']
