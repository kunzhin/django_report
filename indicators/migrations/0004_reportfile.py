# Generated by Django 3.2.8 on 2022-03-28 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0003_auto_20220327_2029'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True, verbose_name='Дата загрузки')),
                ('nkz', models.FileField(blank=True, upload_to='indicators/report07', verbose_name='Новокузнецк')),
                ('nsk', models.FileField(blank=True, upload_to='indicators/report07', verbose_name='Новосибирск')),
                ('omsk', models.FileField(blank=True, upload_to='indicators/report07', verbose_name='Омск')),
                ('krs', models.FileField(blank=True, upload_to='indicators/report07', verbose_name='Красноярск')),
                ('abk', models.FileField(blank=True, upload_to='indicators/report07', verbose_name='Абакан')),
            ],
            options={
                'verbose_name': 'Загрузка отчетов',
                'verbose_name_plural': 'Загрузка отчетов',
            },
        ),
    ]
