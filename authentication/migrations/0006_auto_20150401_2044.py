# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_auto_20150401_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='followees',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
