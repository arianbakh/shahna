# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-02-03 17:58
from __future__ import unicode_literals

import account.models
import datetime
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
            options={
                'verbose_name': 'User Block',
                'verbose_name_plural': 'User Blocks',
            },
        ),
        migrations.CreateModel(
            name='NewUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_creation_date', models.DateTimeField(default=datetime.datetime.now)),
                ('verification_key', models.CharField(default='', max_length=40, verbose_name='verification key')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'New user email',
                'verbose_name_plural': 'New user emails',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, default='avatars/default.jpeg', max_length=255, null=True, upload_to=account.models._avatar_file_name, verbose_name='Avatar')),
                ('name', models.CharField(blank=True, max_length=15, null=True, verbose_name='Name')),
                ('nickname', models.CharField(blank=True, max_length=15, null=True, verbose_name='Nickname (Display name)')),
                ('phone', models.CharField(blank=True, max_length=15, null=True, verbose_name='Mobile phone')),
                ('city', models.CharField(blank=True, max_length=15, null=True, verbose_name='Current city')),
                ('country', models.CharField(blank=True, max_length=15, null=True, verbose_name='Current country')),
                ('university', models.CharField(blank=True, max_length=50, null=True, verbose_name='Graduated university')),
                ('current_work_place', models.CharField(blank=True, max_length=50, null=True, verbose_name='Current work place')),
                ('student_number', models.PositiveIntegerField(blank=True, null=True, verbose_name='Student number')),
                ('stars', models.PositiveIntegerField(default=0, verbose_name='Stars')),
                ('access_level', models.CharField(choices=[('N', 'New'), ('J', 'Rejected'), ('A', 'Accepted')], max_length=1, verbose_name='User access level')),
                ('university_field', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='forum.UniversityField', verbose_name='Field')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
    ]
