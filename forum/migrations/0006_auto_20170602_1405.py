# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-02 14:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_answer_upload_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.CharField(max_length=60, verbose_name='Title'),
        ),
    ]
