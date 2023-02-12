from django.db import models
from django.urls import reverse


class Info(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название новости')
    content = models.TextField(blank=True, verbose_name='Текст новости')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')
    photo = models.ImageField(upload_to='news_photos/%Y/%m/%d/', verbose_name='Фото', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    is_fixed = models.BooleanField(default=False, verbose_name='Закреплено')

    # Получаем абсолютною ссылку на запись модели
    def get_absolute_url(self):
        return reverse("info_item", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Информация'
        verbose_name_plural = 'Информация'
        ordering = ['-is_fixed', '-created_at']