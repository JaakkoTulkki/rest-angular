# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0005_auto_20150401_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='following_campaign',
            field=models.ManyToManyField(related_name='cause_comp_followees', to='causes.Cause', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='company',
            name='following_user',
            field=models.ManyToManyField(related_name='user_comp_followees', to=settings.AUTH_USER_MODEL, null=True, blank=True),
            preserve_default=True,
        ),
    ]
