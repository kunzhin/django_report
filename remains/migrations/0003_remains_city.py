# Generated by Django 3.2.8 on 2022-03-20 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('remains', '0002_remainsfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='remains',
            name='city',
            field=models.CharField(db_column='Город', default='Новокузнецк', max_length=50, verbose_name='Город'),
            preserve_default=False,
        ),
    ]
