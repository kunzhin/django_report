# Generated by Django 3.2.8 on 2022-05-07 04:40

from django.db import migrations, models
import functools
import remains.models


class Migration(migrations.Migration):

    dependencies = [
        ('remains', '0005_remains_topx'),
    ]

    operations = [
        migrations.AddField(
            model_name='remainsfile',
            name='abk_expiration',
            field=models.FileField(blank=True, upload_to=functools.partial(remains.models._update_filename, *(), **{'file': 'expiration', 'path': 'remains', 'place': 'abk'}), verbose_name='Сроки Абакан'),
        ),
        migrations.AddField(
            model_name='remainsfile',
            name='abk_transit',
            field=models.FileField(blank=True, upload_to=functools.partial(remains.models._update_filename, *(), **{'file': 'transit', 'path': 'remains', 'place': 'abk'}), verbose_name='Транзиты Абакан'),
        ),
        migrations.AddField(
            model_name='remainsfile',
            name='krs_expiration',
            field=models.FileField(blank=True, upload_to=functools.partial(remains.models._update_filename, *(), **{'file': 'expiration', 'path': 'remains', 'place': 'krs'}), verbose_name='Сроки Красноярск'),
        ),
        migrations.AddField(
            model_name='remainsfile',
            name='krs_transit',
            field=models.FileField(blank=True, upload_to=functools.partial(remains.models._update_filename, *(), **{'file': 'transit', 'path': 'remains', 'place': 'krs'}), verbose_name='Транзиты Красноярск'),
        ),
        migrations.AddField(
            model_name='remainsfile',
            name='nkz_expiration',
            field=models.FileField(blank=True, upload_to=functools.partial(remains.models._update_filename, *(), **{'file': 'expiration', 'path': 'remains', 'place': 'nkz'}), verbose_name='Сроки Новокузнецк'),
        ),
        migrations.AddField(
            model_name='remainsfile',
            name='nkz_transit',
            field=models.FileField(blank=True, upload_to=functools.partial(remains.models._update_filename, *(), **{'file': 'transit', 'path': 'remains', 'place': 'nkz'}), verbose_name='Транзиты Новокузнецк'),
        ),
        migrations.AddField(
            model_name='remainsfile',
            name='nsk_expiration',
            field=models.FileField(blank=True, upload_to=functools.partial(remains.models._update_filename, *(), **{'file': 'expiration', 'path': 'remains', 'place': 'nsk'}), verbose_name='Сроки Новосибирск'),
        ),
        migrations.AddField(
            model_name='remainsfile',
            name='nsk_transit',
            field=models.FileField(blank=True, upload_to=functools.partial(remains.models._update_filename, *(), **{'file': 'transit', 'path': 'remains', 'place': 'nsk'}), verbose_name='Транзиты Новосибирск'),
        ),
        migrations.AddField(
            model_name='remainsfile',
            name='omsk_expiration',
            field=models.FileField(blank=True, upload_to=functools.partial(remains.models._update_filename, *(), **{'file': 'expiration', 'path': 'remains', 'place': 'omsk'}), verbose_name='Сроки Омск'),
        ),
        migrations.AddField(
            model_name='remainsfile',
            name='omsk_transit',
            field=models.FileField(blank=True, upload_to=functools.partial(remains.models._update_filename, *(), **{'file': 'transit', 'path': 'remains', 'place': 'omsk'}), verbose_name='Транзиты Омск'),
        ),
        migrations.AlterField(
            model_name='remainsfile',
            name='abk',
            field=models.FileField(blank=True, upload_to=functools.partial(remains.models._update_filename, *(), **{'file': 'remains', 'path': 'remains', 'place': 'abk'}), verbose_name='Главный склад Абакан'),
        ),
        migrations.AlterField(
            model_name='remainsfile',
            name='krs',
            field=models.FileField(blank=True, upload_to=functools.partial(remains.models._update_filename, *(), **{'file': 'remains', 'path': 'remains', 'place': 'krs'}), verbose_name='Главный склад Красноярск'),
        ),
        migrations.AlterField(
            model_name='remainsfile',
            name='nkz',
            field=models.FileField(blank=True, upload_to=functools.partial(remains.models._update_filename, *(), **{'file': 'remains', 'path': 'remains', 'place': 'nkz'}), verbose_name='Главный склад Новокузнецк'),
        ),
        migrations.AlterField(
            model_name='remainsfile',
            name='nsk',
            field=models.FileField(blank=True, upload_to=functools.partial(remains.models._update_filename, *(), **{'file': 'remains', 'path': 'remains', 'place': 'nsk'}), verbose_name='Главный склад Новосибирск'),
        ),
        migrations.AlterField(
            model_name='remainsfile',
            name='omsk',
            field=models.FileField(blank=True, upload_to=functools.partial(remains.models._update_filename, *(), **{'file': 'remains', 'path': 'remains', 'place': 'omsk'}), verbose_name='Главный склад Омск'),
        ),
    ]