# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('causes', '0001_initial'),
        ('values', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('company_name', models.CharField(unique=True, max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('about', models.TextField(null=True, blank=True)),
                ('founded', models.DateField(null=True, blank=True)),
                ('country', models.CharField(null=True, max_length=100, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('mission', models.TextField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('likes', models.IntegerField(default=0)),
                ('account_owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('following_cause', models.ManyToManyField(null=True, to='causes.Cause', related_name='cause_comp_followees', blank=True)),
                ('following_company', models.ManyToManyField(null=True, to='companies.Company', related_name='comp_followees', blank=True)),
                ('following_user', models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL, related_name='user_comp_followees', blank=True)),
                ('values', models.ManyToManyField(to='values.Value')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.TextField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('price', models.FloatField()),
                ('owner', models.ForeignKey(to='companies.Company', related_name='products')),
                ('values', models.ManyToManyField(to='values.Value')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together=set([('owner', 'name')]),
        ),
    ]
