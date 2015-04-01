# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='following',
            field=models.ManyToManyField(related_name='followees', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
