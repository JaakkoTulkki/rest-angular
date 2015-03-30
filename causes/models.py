from django.db import models

# Create your models here.


class Cause(models.Model):
    creator = models.ForeignKey('authentication.Account')
    name = models.CharField(max_length=100)
    sponsors = models.ManyToManyField('companies.Company')
    slug = models.SlugField(unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    values = models.ManyToManyField('values.Value')
    url = models.URLField(blank=True, null=True)
    likes = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    followers = models.ManyToManyField('authentication.Account', related_name='cause_following')

class CauseMembers(models.Model):
    """
    A company can be a member of a Cause
    """
    company = models.ForeignKey('companies.Company', related_name='Causes')
    cause = models.ForeignKey('causes.Cause', related_name='members')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Joined Cause")
    updated_at = models.DateTimeField(auto_now=True)
    products = models.ManyToManyField('companies.Product')
    class Meta:
        unique_together = (('company', 'cause'),)