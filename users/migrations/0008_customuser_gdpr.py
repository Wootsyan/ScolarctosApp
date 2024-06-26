# Generated by Django 4.2.4 on 2024-02-22 22:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gdpr', '0002_rename_gdpr_gdpr_gdpr_consent'),
        ('users', '0007_rename_data_joined_customuser_date_joined'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='gdpr',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gdpr', to='gdpr.gdpr'),
        ),
    ]
