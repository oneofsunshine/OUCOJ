# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-05-01 04:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20171125_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='admin_type',
            field=models.TextField(default='Regular User'),
        ),
        migrations.AlterField(
            model_name='user',
            name='auth_token',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='open_api_appkey',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='problem_permission',
            field=models.TextField(default='None'),
        ),
        migrations.AlterField(
            model_name='user',
            name='reset_password_token',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='tfa_token',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.TextField(unique=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.TextField(default='/public/avatar/default.png'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='blog',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='github',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='major',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='mood',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='real_name',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='school',
            field=models.TextField(null=True),
        ),
    ]
