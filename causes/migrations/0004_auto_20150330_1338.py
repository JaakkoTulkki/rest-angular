# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('companies', '0001_initial'),
        ('values', '0001_initial'),
        ('causes', '0003_auto_20150329_2008'),
    ]

    operations = [
        migrations.AddField(
            model_name='cause',
            name='followers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='cause_following'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cause',
            name='sponsors',
            field=models.ManyToManyField(to='companies.Company'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cause',
            name='values',
            field=models.ManyToManyField(to='values.Value'),
            preserve_default=True,
        ),
    ]
