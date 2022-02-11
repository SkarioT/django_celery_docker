# Generated by Django 4.0.2 on 2022-02-11 14:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('sender', '0002_alter_messageinfo_create_alter_send_out_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messageinfo',
            name='status',
            field=models.CharField(default='False', max_length=100, verbose_name='статус отправки'),
        ),
        migrations.AlterField(
            model_name='send_out',
            name='end',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 11, 15, 15, 35, 201904, tzinfo=utc), verbose_name='дата и время завершения рассылки'),
        ),
    ]