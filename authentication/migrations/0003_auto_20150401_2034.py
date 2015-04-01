# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_account_following'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='following',
        ),
        migrations.AddField(
            model_name='account',
            name='followees',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='followers'),
            preserve_default=True,
        ),
    ]
