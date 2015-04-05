from django.db import models
from django.utils.text import slugify
from kehko.models import UniqueSlugMixin

class Company(models.Model):
    account_owner = models.ForeignKey('authentication.Account')
    company_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    about = models.TextField(null=True, blank=True)
    founded = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    mission = models.TextField(null=True, blank=True)
    #companies can follow different stuff as well
    following_company = models.ManyToManyField('self', related_name='comp_followees', symmetrical=False, null=True, blank=True)
    following_user = models.ManyToManyField('authentication.Account', related_name='user_comp_followees', symmetrical=False, null=True, blank=True)
    following_cause = models.ManyToManyField('causes.Cause', related_name='cause_comp_followees', symmetrical=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    likes = models.IntegerField(default=0)
    values = models.ManyToManyField('values.Value')

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.company_name)
        super(Company, self).save(*args, **kwargs)


class Product(models.Model):
    owner = models.ForeignKey('companies.Company', related_name='products')
    name = models.TextField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField()
    values = models.ManyToManyField('values.Value')

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.owner.company_name + ' ' +self.name)
        super(Product, self).save(*args, **kwargs)

    class Meta:
        unique_together = (('owner', 'name'),)