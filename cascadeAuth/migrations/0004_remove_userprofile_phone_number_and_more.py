# Generated by Django 5.0.6 on 2024-07-03 05:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cascadeAuth', '0003_userprofile_security_answer_2_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='security_answer_3',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='security_question_3',
        ),
    ]
