# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-23 10:24
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='head',
            field=models.ImageField(default='head/memtx.png', upload_to='head/%Y%m', verbose_name='用户头像'),
        ),
        migrations.AlterField(
            model_name='users',
            name='num',
            field=models.CharField(max_length=11, validators=[django.core.validators.MinLengthValidator(11, '手机号码必须为11位'), django.core.validators.RegexValidator('^1[3-9]\\d{9}$', '手机号码格式错误!')]),
        ),
    ]
