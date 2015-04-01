# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0004_auto_20150331_1610'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='full_name',
            new_name='company_name',
        ),
    ]
