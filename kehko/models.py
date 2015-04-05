from django.db import models
from django.utils.text import slugify

class KehkoModel():
    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)