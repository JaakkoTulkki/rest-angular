# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0001_initial'),
        ('values', '0001_initial'),
        ('causes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='causemembers',
            name='company',
            field=models.ForeignKey(to='companies.Company', related_name='Causes'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='causemembers',
            name='products',
            field=models.ManyToManyField(to='companies.Product'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='causemembers',
            unique_together=set([('company', 'cause')]),
        ),
        migrations.AddField(
            model_name='cause',
            name='creator',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cause',
            name='followers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='cause_following'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cause',
            name='sponsors',
            field=models.ManyToManyField(to='companies.Company'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cause',
            name='values',
            field=models.ManyToManyField(to='values.Value'),
            preserve_default=True,
        ),
    ]
