# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('causes', '0001_initial'),
        ('authentication', '0001_initial'),
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='liked_causes',
            field=models.ManyToManyField(null=True, to='causes.Cause', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='liked_companies',
            field=models.ManyToManyField(null=True, to='companies.Company', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='liked_products',
            field=models.ManyToManyField(null=True, to='companies.Product', blank=True),
            preserve_default=True,
        ),
    ]
