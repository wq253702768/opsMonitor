# Generated by Django 2.2 on 2020-01-10 12:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0008_monitortask_recover_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitortask',
            name='c_time',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2020, 1, 10, 12, 22, 8, 562042, tzinfo=utc), verbose_name='报警时间'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='monitortask',
            name='u_time',
            field=models.DateTimeField(auto_now=True, verbose_name='恢复时间'),
        ),
    ]
