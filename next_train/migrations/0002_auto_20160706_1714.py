# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-06 21:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('next_train', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stationprefs',
            name='station',
            field=models.TextField(max_length=300),
        ),
    ]
