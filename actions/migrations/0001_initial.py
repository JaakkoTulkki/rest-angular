# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('causes', '0004_auto_20150405_2142'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('url', models.URLField()),
                ('cause_member', models.ForeignKey(to='causes.CauseMembers')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
