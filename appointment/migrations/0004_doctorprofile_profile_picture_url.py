# Generated by Django 5.1.3 on 2025-03-09 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0003_alter_appointmentdetail_prescription'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorprofile',
            name='profile_picture_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
