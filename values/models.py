from django.db import models
from django.utils.text import slugify

from kehko.models import UniqueSlugMixin

# Create your models here.
class Value(UniqueSlugMixin, models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)
