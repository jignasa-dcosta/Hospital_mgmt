# Generated by Django 5.1.3 on 2025-01-22 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0002_doctorprofile_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointmentdetail',
            name='prescription',
            field=models.TextField(blank=True, null=True),
        ),
    ]
