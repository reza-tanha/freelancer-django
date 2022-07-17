# Generated by Django 4.0.5 on 2022-07-15 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='uuid',
        ),
        migrations.AddField(
            model_name='project',
            name='publish',
            field=models.CharField(choices=[('publish', 'منتشر شد'), ('rejection', 'رد شد'), ('wait', 'منتظر تایید ادمین')], default='wait', max_length=30, verbose_name='انتشار پروژه'),
        ),
    ]