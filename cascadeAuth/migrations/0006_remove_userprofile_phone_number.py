# Generated by Django 5.0.6 on 2024-07-03 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cascadeAuth', '0005_userprofile_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='phone_number',
        ),
    ]
