# Generated by Django 4.0.2 on 2022-02-12 08:18

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('sender', '0005_alter_messageinfo_status_alter_send_out_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='send_out',
            name='end',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 12, 9, 18, 34, 147642, tzinfo=utc), verbose_name='дата и время завершения рассылки'),
        ),
    ]