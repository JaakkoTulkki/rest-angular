# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0002_auto_20150323_2118'),
    ]

    operations = [
        migrations.RenameField(
            model_name='campaignmembers',
            old_name='member',
            new_name='company',
        ),
        migrations.AlterUniqueTogether(
            name='campaignmembers',
            unique_together=set([('company', 'campaign')]),
        ),
    ]
