# Generated by Django 3.2.8 on 2022-04-30 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0015_taskcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='report07',
            name='code_tt',
            field=models.CharField(db_column='код ТТ', default=1, max_length=255, verbose_name='код ТТ'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='report145',
            name='code_tt',
            field=models.CharField(db_column='ID ТТ', default=1, max_length=255, verbose_name='ID ТТ'),
            preserve_default=False,
        ),
    ]
