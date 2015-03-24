# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('values', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('likes', models.IntegerField(default=0)),
                ('account_owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('following_campaign', models.ManyToManyField(to='campaigns.Campaign', related_name='camp_followees')),
                ('following_company', models.ManyToManyField(to='companies.Company', related_name='comp_followees')),
                ('following_user', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='user_followees')),
                ('values', models.ManyToManyField(to='values.Value')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.TextField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField()),
                ('price', models.FloatField()),
                ('owner', models.ForeignKey(to='companies.Company', related_name='products')),
                ('values', models.ManyToManyField(to='values.Value')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
