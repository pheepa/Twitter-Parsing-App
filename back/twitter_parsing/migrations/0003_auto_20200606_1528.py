# Generated by Django 3.0.7 on 2020-06-06 12:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_parsing', '0002_auto_20200606_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inquiry',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Дата запроса'),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='date',
            field=models.DateTimeField(blank=True, verbose_name='дата публикации'),
        ),
    ]
