# Generated by Django 4.2.4 on 2024-02-09 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_alter_teamtutor_confirmation_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='editable',
            field=models.BooleanField(default=True),
        ),
    ]
