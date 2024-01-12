# Generated by Django 4.2.4 on 2024-01-10 21:51

from django.db import migrations
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from users.models import CustomGroup

def add_groups_and_permissions(apps, schema_editor):
    for group_name in CustomGroup.names:
        Group.objects.create(name=group_name)
    

def remove_groups_and_permissions(apps, schema_editor):
    for group_name in CustomGroup.names:
        Group.objects.filter(name=group_name).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_customuser_options_and_more'),
    ]

    operations = [
        migrations.RunPython(code=add_groups_and_permissions, reverse_code=remove_groups_and_permissions),
    ]