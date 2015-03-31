# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('values', '0002_value_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='value',
            name='name',
            field=models.CharField(unique=True, max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='value',
            name='slug',
            field=models.SlugField(unique=True),
            preserve_default=True,
        ),
    ]
