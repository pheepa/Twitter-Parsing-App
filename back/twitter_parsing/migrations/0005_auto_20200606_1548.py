# Generated by Django 3.0.7 on 2020-06-06 12:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_parsing', '0004_auto_20200606_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='date',
            field=models.DateField(default=datetime.date(2020, 6, 6), verbose_name='дата публикации'),
        ),
        migrations.AlterField(
            model_name='inquiry',
            name='date',
            field=models.DateField(default=datetime.date(2020, 6, 6), verbose_name='Дата запроса'),
        ),
    ]
