# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-23 18:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20190123_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='goodsclassmodel',
            name='classname',
            field=models.CharField(default='', max_length=6, verbose_name='分类名'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='goodsskuclassmodel',
            name='goodsintro',
            field=models.CharField(default='', max_length=30, verbose_name='商品简介'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='goodsskuclassmodel',
            name='goodsname',
            field=models.CharField(default='', max_length=10, verbose_name='商品名'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='goodsskuclassmodel',
            name='goodsprice',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='价格'),
            preserve_default=False,
        ),
    ]