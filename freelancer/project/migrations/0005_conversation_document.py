# Generated by Django 4.0.5 on 2022-08-03 16:38

from django.db import migrations, models
import freelancer.project.models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_conversation_delete_conversationmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='document',
            field=models.FileField(blank=True, null=True, upload_to=freelancer.project.models.document_directory_path, verbose_name='فایل'),
        ),
    ]
