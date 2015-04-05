# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='about',
        ),
        migrations.RemoveField(
            model_name='company',
            name='country',
        ),
        migrations.RemoveField(
            model_name='company',
            name='description',
        ),
        migrations.RemoveField(
            model_name='company',
            name='following_cause',
        ),
        migrations.RemoveField(
            model_name='company',
            name='following_company',
        ),
        migrations.RemoveField(
            model_name='company',
            name='following_user',
        ),
        migrations.RemoveField(
            model_name='company',
            name='founded',
        ),
        migrations.RemoveField(
            model_name='company',
            name='mission',
        ),
    ]
