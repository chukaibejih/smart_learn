# Generated by Django 4.1 on 2023-07-05 16:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_service', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='lesson_documents',
            field=models.FileField(blank=True, null=True, upload_to='lesson_documents/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'docx', 'doc', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7zip'])]),
        ),
        migrations.AddField(
            model_name='lesson',
            name='lesson_video',
            field=models.FileField(blank=True, null=True, upload_to='lesson_videos/', validators=[django.core.validators.FileExtensionValidator(['mp4', 'mkv', 'wmv', '3gp', 'f4v', 'avi', 'mp3'])]),
        ),
    ]