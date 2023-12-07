# Generated by Django 4.2.4 on 2023-11-30 23:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_user_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'user'},
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(default=None, max_length=9, null=True, unique=True, validators=[django.core.validators.MinLengthValidator]),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Uczeń'), (2, 'Opiekun'), (3, 'Organizator'), (4, 'Administrator')], default=1),
        ),
    ]