# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0003_auto_20150331_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='following_campaign',
            field=models.ManyToManyField(null=True, blank=True, related_name='cause_followees', to='causes.Cause'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='company',
            name='following_company',
            field=models.ManyToManyField(null=True, blank=True, related_name='comp_followees', to='companies.Company'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='company',
            name='following_user',
            field=models.ManyToManyField(null=True, blank=True, related_name='user_followees', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
