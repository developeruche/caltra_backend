# Generated by Django 3.1.8 on 2021-11-20 22:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0002_auto_20211120_2308'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answers',
            old_name='question_video',
            new_name='answer_video',
        ),
    ]
