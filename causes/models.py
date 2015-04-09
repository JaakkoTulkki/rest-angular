from django.db import models
from django.utils.text import slugify
# Create your models here.
from kehko.models import UniqueSlugMixin

class Cause(UniqueSlugMixin, models.Model):
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
    #followers, people following this cause => Jesus had followers, causes have followers
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
    mission_statement = models.TextField(null=True, blank=True)

    @property
    def _cause_name(self):
        return self.cause.name
    cause_name = _cause_name

    class Meta:
        unique_together = (('company', 'cause'),)