# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('causes', '0003_auto_20150405_2142'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='causemembers',
            unique_together=set([('company', 'cause')]),
        ),
    ]
