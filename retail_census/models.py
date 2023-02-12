import sys
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from accounts.models import DSM, TSM, ESR
from indicators.models import ChannelTT
from PIL import Image, ImageOps
from io import BytesIO


class PresenceNestle(models.Model):
    presenceNestle = models.CharField(max_length=255, blank=False,
                                      verbose_name='Ассортимент Nestle')

    def __str__(self) -> str:
        return self.presenceNestle

    class Meta:
        verbose_name = 'Ассортимент Nestle'
        verbose_name_plural = 'Ассортимент Nestle'


class Competitors(models.Model):
    competitors = models.CharField(max_length=255, blank=False,
                                   verbose_name='Конкуренты')

    def __str__(self) -> str:
        return self.competitors
   
    class Meta:
        verbose_name = 'Конкурент'
        verbose_name_plural = 'Конкуренты'


class Outlet(models.Model):
    WTC = [
        ('', 'Выбери'),
        ('Ассортимент не интересен', 'Ассортимент не интересен'),
        ('Не проходим по цене', 'Не проходим по цене'),
        ('Оставили прайс', 'Оставили прайс'),
        ('Заводим договор поставки', 'Заводим договор поставки'),
        ('Работаем', 'Работаем'),
    ]
    
    #taxIdentificationNumberRegex = RegexValidator(regex=r"/^\d+$/")
    #phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")

    dsm = models.ForeignKey(DSM, on_delete=models.PROTECT, null=False, verbose_name='Территория DSM')
    tsm = models.ForeignKey(TSM, on_delete=models.PROTECT, null=False, verbose_name='Территория TSM')
    esr = models.ForeignKey(ESR, on_delete=models.PROTECT, null=False, verbose_name='Территория ESR')
    corporateBodyName = models.CharField(max_length=255, blank=False, verbose_name='Наименование юр.лица')
    taxIdentificationNumber = models.CharField(max_length=12, blank=True, verbose_name='ИНН')
    count_tt = models.IntegerField(default=1, verbose_name='Кол-во ТТ')
    contactName = models.CharField(max_length=255, blank=True, verbose_name='Контактное лицо')
    phoneNumber = models.CharField(max_length=16, blank=True, verbose_name='Номер телефона')
    deliveryContract = models.BooleanField(default=False, verbose_name='Договор поставки с ООО КОНТИНЕНТ')
    name_tt = models.CharField(max_length=255, blank=False, verbose_name='Наименование ТТ')
    city = models.CharField(max_length=255, blank=False, verbose_name='Город')
    street = models.CharField(max_length=255, blank=False, verbose_name='Улица')
    houseNumber = models.CharField(max_length=10, blank=False, verbose_name='Номер дома')
    channel_tt = models.ForeignKey(ChannelTT, on_delete=models.PROTECT, null=False, verbose_name='Канал ТТ')
    photo = models.ImageField(blank=False, upload_to='outlet_photos/%Y/%m/%d', verbose_name='Фото вывески')
    presenceNestle = models.ManyToManyField(PresenceNestle, default='Нет ассортимента Nestle')
    competitors = models.ManyToManyField(Competitors, default='Нет конкурентов')
    comment = models.TextField(blank=True, verbose_name='Дополнительные заметки')
    dateConversation = models.DateTimeField(blank=False, verbose_name='Дата следующего визита')
    statusWorkedOut = models.CharField(max_length=255, blank=False, choices=WTC, verbose_name='Статус')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата записи')
    updated_at = models.DateField(auto_now=True, verbose_name='Дата обновления')

    # Получаем абсолютною ссылку на запись модели
    def get_absolute_url(self):
        return reverse("view_outlet", kwargs={"pk": self.pk})

    def get_tsm_dsm(self):
        esr = ESR.objects.get(esr=self.esr)
        tsm = TSM.objects.get(tsm=esr.tsm)
        self.tsm = esr.tsm
        self.dsm = tsm.dsm

    # Переопределенный метод save() для сохранения DSM, TSM и сжатия фото.
    def save(self, *args, **kwargs):
        # Присваиваем территории DSM, TSM
        self.get_tsm_dsm()

        # Открываем загруженное фото
        im = Image.open(self.photo)
        im = ImageOps.exif_transpose(im)

        output = BytesIO()

        (width, height) = (im.width // 2, im.height // 2)
        im = im.resize((width, height))
        im.save(output, format='JPEG', quality=80)
        output.seek(0)
        self.photo = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.photo.name.split('.')[0],
                                          'image/jpeg', sys.getsizeof(output), None)

        super(Outlet, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name_tt

    class Meta:
        verbose_name = 'Торговая точка'
        verbose_name_plural = 'Торговые точки'
        ordering = ['-dateConversation']


@receiver(pre_delete, sender=Outlet)
def file_model_delete(sender, instance, **kwargs):
    if instance.photo.name:
        instance.photo.delete(False)