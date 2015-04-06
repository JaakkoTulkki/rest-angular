# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20150406_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='date_of_birth',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
