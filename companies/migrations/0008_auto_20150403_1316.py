# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0007_auto_20150401_1201'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='product',
            unique_together=set([('owner', 'name')]),
        ),
    ]
