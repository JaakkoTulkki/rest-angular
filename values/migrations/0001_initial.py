# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import kehko.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('slug', models.SlugField(unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('likes', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(kehko.models.UniqueSlugMixin, models.Model),
        ),
    ]
