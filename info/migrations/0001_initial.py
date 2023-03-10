# Generated by Django 3.2.8 on 2022-03-19 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название новости')),
                ('content', models.TextField(blank=True, verbose_name='Текст новости')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')),
                ('photo', models.ImageField(blank=True, upload_to='news_photos/%Y/%m/%d/', verbose_name='Фото')),
                ('is_published', models.BooleanField(default=True, verbose_name='Публикация')),
                ('is_fixed', models.BooleanField(default=False, verbose_name='Закреплено')),
            ],
            options={
                'verbose_name': 'Информация',
                'verbose_name_plural': 'Информация',
                'ordering': ['-is_fixed', '-created_at'],
            },
        ),
    ]
