# Generated by Django 3.2.8 on 2022-07-05 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('remains', '0006_auto_20220507_1140'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suspended',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dbc', models.CharField(db_column='DBC', max_length=255, verbose_name='DBC')),
                ('code_nestle', models.IntegerField(db_column='код товара', verbose_name='Код товара')),
                ('status', models.CharField(db_column='status', max_length=255, verbose_name='Статус позиции')),
            ],
            options={
                'verbose_name': 'Позиция на вывод',
                'verbose_name_plural': 'Позиции на вывод',
            },
        ),
        migrations.AddField(
            model_name='remains',
            name='status',
            field=models.CharField(db_column='status', default='', max_length=255, verbose_name='Статус позиции'),
            preserve_default=False,
        ),
    ]
