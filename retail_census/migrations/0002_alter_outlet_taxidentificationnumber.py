# Generated by Django 3.2.8 on 2022-06-21 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retail_census', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outlet',
            name='taxIdentificationNumber',
            field=models.CharField(blank=True, max_length=12, verbose_name='ИНН'),
        ),
    ]
