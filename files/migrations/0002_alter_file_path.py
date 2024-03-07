# Generated by Django 4.2.4 on 2024-03-06 22:19

from django.db import migrations, models
import files.utils


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='path',
            field=models.FileField(max_length=254, upload_to=files.utils.file_directory_path),
        ),
    ]
