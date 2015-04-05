# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('causes', '0004_auto_20150405_2142'),
        ('companies', '0002_auto_20150405_2151'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='about',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='country',
            field=models.CharField(null=True, blank=True, max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='description',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='following_cause',
            field=models.ManyToManyField(null=True, to='causes.Cause', blank=True, related_name='cause_comp_followees'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='following_company',
            field=models.ManyToManyField(null=True, to='companies.Company', blank=True, related_name='comp_followees'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='following_user',
            field=models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL, blank=True, related_name='user_comp_followees'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='founded',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='mission',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
