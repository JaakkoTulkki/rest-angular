import os
import uuid

from django.db import models
from django.utils.text import slugify

# Create your models here.
class Image(models.Model):
    def get_file_path(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return "new-photos/"+filename

    uploader = models.ForeignKey('authentication.Account')
    company = models.ForeignKey('companies.Company', blank=True, null=True)
    name = models.CharField(max_length=160)
    image = models.ImageField(upload_to=get_file_path)
