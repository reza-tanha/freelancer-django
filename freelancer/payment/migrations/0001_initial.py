# Generated by Django 4.0.5 on 2022-07-22 07:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ پرداخت')),
                ('authority', models.CharField(max_length=120, verbose_name='توکن خرید')),
                ('paid', models.BooleanField(default=False, verbose_name='پرداخت شده ؟')),
                ('price', models.IntegerField(verbose_name='مبلغ(ریال)')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_pay', to='project.project', verbose_name='پروژه')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_project_pay', to=settings.AUTH_USER_MODEL, verbose_name='پرداخت کننده')),
            ],
            options={
                'verbose_name': 'Project Payment',
                'verbose_name_plural': 'Projects Payments',
            },
        ),
        migrations.CreateModel(
            name='PaymentAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ پرداخت')),
                ('authority', models.CharField(max_length=120, verbose_name='توکن خرید')),
                ('payed', models.BooleanField(default=False, verbose_name='پرداخت شده ؟')),
                ('price', models.IntegerField(verbose_name='مبلغ(ریال)')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_account_pay', to=settings.AUTH_USER_MODEL, verbose_name='پرداخت کننده')),
            ],
            options={
                'verbose_name': 'User Payment',
                'verbose_name_plural': 'User Payments',
            },
        ),
    ]
