# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import images.models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_image_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to=images.models.Image.get_file_path),
            preserve_default=True,
        ),
    ]
