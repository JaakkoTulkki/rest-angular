from django.db import models

from authentication.models import Account
from companies.models import Company, Product
from values.models import Value

# Create your models here.

class Campaign(models.Model):
    creator = models.ForeignKey(Account)
    name = models.CharField(max_length=100)
    sponsors = models.ManyToManyField(Company)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    values = models.ManyToManyField(Value)
    url = models.URLField(blank=True, null=True)
    likes = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    followers = models.ManyToManyField(Account, related_name='camp_following', symmetrical=False)

class CampaignMembers(models.Model):
    """
    A company can be a member of a campaign
    """
    member = models.ForeignKey(Company, related_name='campaigns')
    campaign = models.ForeignKey(Campaign, related_name='members')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Joined campaign")
    updated_at = models.DateTimeField(auto_now=True)
    products = models.ManyToManyField(Product)
    class Meta:
        unique_together = (('member', 'campaign'),)