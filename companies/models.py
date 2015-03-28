from django.db import models

class Company(models.Model):
    account_owner = models.ForeignKey('authentication.Account')
    full_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    following_company = models.ManyToManyField('self', related_name='comp_followees', symmetrical=False)
    following_user = models.ManyToManyField('authentication.Account', related_name='user_followees', symmetrical=False)
    following_campaign = models.ManyToManyField('causes.Cause', related_name='cause_followees', symmetrical=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    likes = models.IntegerField(default=0)
    values = models.ManyToManyField('values.Value')

class Product(models.Model):
    owner = models.ForeignKey('companies.Company', related_name='products')
    name = models.TextField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.FloatField()
    values = models.ManyToManyField('values.Value')