# Generated by Django 3.2.8 on 2022-03-27 03:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20220327_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='esr',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='accounts.esr', verbose_name='Территория ESR'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='tsm',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='accounts.tsm', verbose_name='Территория TSM'),
        ),
    ]
