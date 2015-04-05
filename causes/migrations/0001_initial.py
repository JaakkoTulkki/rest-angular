# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import kehko.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cause',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('url', models.URLField(null=True, blank=True)),
                ('likes', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(kehko.models.UniqueSlugMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CauseMembers',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created_at', models.DateTimeField(verbose_name='Joined Cause', auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('mission_statement', models.TextField(null=True, blank=True)),
                ('cause', models.ForeignKey(to='causes.Cause', related_name='members')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
