# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_auto_20150331_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='following_campaign',
            field=models.ManyToManyField(to='causes.Cause', related_name='cause_followees', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='company',
            name='following_company',
            field=models.ManyToManyField(to='companies.Company', related_name='comp_followees', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='company',
            name='following_user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='user_followees', blank=True),
            preserve_default=True,
        ),
    ]
