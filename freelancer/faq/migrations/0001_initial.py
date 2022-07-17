# Generated by Django 4.0.5 on 2022-07-14 15:38

from django.db import migrations, models
import django_quill.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=100, verbose_name='متن سوال')),
                ('answer', django_quill.fields.QuillField(max_length=20000, verbose_name='جواب سوال')),
                ('position', models.PositiveSmallIntegerField(unique=True, verbose_name='یک عدد صحیح برای مرتب کردن سوال در میان سایر سوالات')),
            ],
        ),
    ]