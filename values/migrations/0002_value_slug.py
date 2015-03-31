# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('values', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='value',
            name='slug',
            field=models.SlugField(default='value'),
            preserve_default=False,
        ),
    ]
