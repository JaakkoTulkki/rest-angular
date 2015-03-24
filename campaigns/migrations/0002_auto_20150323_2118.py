# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('companies', '0001_initial'),
        ('values', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaignmembers',
            name='member',
            field=models.ForeignKey(to='companies.Company', related_name='campaigns'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='campaignmembers',
            name='products',
            field=models.ManyToManyField(to='companies.Product'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='campaignmembers',
            unique_together=set([('member', 'campaign')]),
        ),
        migrations.AddField(
            model_name='campaign',
            name='creator',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='campaign',
            name='followers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='camp_following'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='campaign',
            name='sponsors',
            field=models.ManyToManyField(to='companies.Company'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='campaign',
            name='values',
            field=models.ManyToManyField(to='values.Value'),
            preserve_default=True,
        ),
    ]
