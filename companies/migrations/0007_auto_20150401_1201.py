# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0006_auto_20150401_1150'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='following_campaign',
            new_name='following_cause',
        ),
    ]
