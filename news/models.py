from django.db import models
from django.utils.text import slugify


class News(models.Model):
    company = models.ForeignKey('companies.Company', related_name="news")
    author = models.ForeignKey('authentication.Account', null=True, blank=True)
    title = models.CharField(max_length=100)
    body = models.TextField()
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.title)
        super(News, self).save(*args, **kwargs)

    def __str__(self):
        return "{}, {}: {}".format(self.company, self.author, self.body)