# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-01-27 16:19
from __future__ import unicode_literals

import account.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('forum', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField(blank=True, default='', null=True, verbose_name='Block reason')),
                ('till_date', models.DateTimeField(verbose_name='Block till')),
                ('unlimited', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(max_length=255, upload_to=account.models._avatar_file_name, verbose_name='Avatar')),
                ('name', models.CharField(max_length=15, verbose_name='Name')),
                ('nickname', models.CharField(max_length=15, verbose_name='Nickname (Display name)')),
                ('phone', models.CharField(max_length=15, verbose_name='Mobile phone')),
                ('city', models.CharField(max_length=15, verbose_name='Current city')),
                ('country', models.CharField(max_length=15, verbose_name='Current country')),
                ('university', models.CharField(max_length=50, verbose_name='Graduated university')),
                ('current_work_place', models.CharField(max_length=50, verbose_name='Current work place')),
                ('student_number', models.PositiveIntegerField(blank=True, null=True, verbose_name='Student number')),
                ('stars', models.PositiveIntegerField(default=0, verbose_name='Stars')),
                ('access_level', models.CharField(choices=[('N', 'New'), ('J', 'Rejected'), ('A', 'Accepted')], max_length=1, verbose_name='User access level')),
                ('university_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.UniversityField', verbose_name='Field')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
