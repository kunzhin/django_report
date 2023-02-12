# Generated by Django 3.2.8 on 2022-03-19 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryRemains',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_category', models.CharField(db_column='Код категории', max_length=3, verbose_name='Код категории')),
                ('category', models.CharField(db_column='Категория', max_length=255, verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Категория остатков',
                'verbose_name_plural': 'Категории остатков',
                'ordering': ['code_category'],
            },
        ),
        migrations.CreateModel(
            name='Remains',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_category', models.CharField(db_column='Код категории', max_length=3, verbose_name='Код категории')),
                ('category', models.CharField(db_column='Категория', max_length=255, verbose_name='Категория')),
                ('code_continent', models.CharField(db_column='Код', max_length=5, verbose_name='Код')),
                ('code_nestle', models.CharField(db_column='Артикул', max_length=8, verbose_name='Артикул')),
                ('nomenclature', models.CharField(db_column='Номенклатура', max_length=255, verbose_name='Номенклатура')),
                ('remaining', models.IntegerField(blank=True, db_column='Остаток', verbose_name='Остаток')),
                ('reserve', models.BigIntegerField(blank=True, db_column='Резерв', verbose_name='Резерв')),
                ('free_remain', models.IntegerField(blank=True, db_column='Свободный остаток', verbose_name='Свободный остаток')),
                ('expiration_date', models.DateField(blank=True, db_column='Срок годности', verbose_name='Срок годности')),
                ('remaining_term', models.CharField(blank=True, db_column='Остаток срока', max_length=5, verbose_name='Остаток срока')),
                ('date_arrival', models.DateField(blank=True, db_column='Дата прихода', verbose_name='Дата прихода')),
                ('transit_box', models.IntegerField(blank=True, db_column='Транзит (Короб)', verbose_name='Транзит (Короб)')),
            ],
            options={
                'verbose_name': 'Остатки',
                'verbose_name_plural': 'Остатки',
                'ordering': ['code_category', '-nomenclature'],
            },
        ),
    ]