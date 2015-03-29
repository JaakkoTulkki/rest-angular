# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('causes', '0002_auto_20150328_2145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cause',
            name='followers',
        ),
        migrations.RemoveField(
            model_name='cause',
            name='sponsors',
        ),
        migrations.RemoveField(
            model_name='cause',
            name='values',
        ),
    ]
