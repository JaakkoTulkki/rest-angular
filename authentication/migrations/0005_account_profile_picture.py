# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
        ('authentication', '0004_auto_20150406_1214'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='profile_picture',
            field=models.ForeignKey(null=True, blank=True, to='images.Image'),
            preserve_default=True,
        ),
    ]
