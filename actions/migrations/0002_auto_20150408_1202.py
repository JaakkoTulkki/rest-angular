# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 8, 12, 2, 32, 998783, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='action',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 4, 8, 12, 2, 43, 831669, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
