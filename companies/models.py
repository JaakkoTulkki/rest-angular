from django.db import models
from django.utils.text import slugify
from kehko.models import KehkoModel

class Company(KehkoModel, models.Model):
    account_owner = models.ForeignKey('authentication.Account')
    company_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    following_company = models.ManyToManyField('self', related_name='comp_followees', symmetrical=False, null=True, blank=True)
    following_user = models.ManyToManyField('authentication.Account', related_name='user_comp_followees', symmetrical=False, null=True, blank=True)
    following_cause = models.ManyToManyField('causes.Cause', related_name='cause_comp_followees', symmetrical=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    likes = models.IntegerField(default=0)
    values = models.ManyToManyField('values.Value')


class Product(KehkoModel, models.Model):
    owner = models.ForeignKey('companies.Company', related_name='products')
    name = models.TextField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.FloatField()
    values = models.ManyToManyField('values.Value')

    class Meta:
        unique_together = (('owner', 'name'),)