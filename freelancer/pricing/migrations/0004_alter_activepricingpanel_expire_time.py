# Generated by Django 4.0.5 on 2022-10-06 11:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pricing', '0003_alter_activepricingpanel_expire_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activepricingpanel',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 5, 11, 20, 3, 829484, tzinfo=utc), verbose_name='تاریخ انقضای پنل'),
        ),
    ]
