from django.db import models

# Create your models here.


class Campaign(models.Model):
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
    followers = models.ManyToManyField('authentication.Account', related_name='camp_following')

class CampaignMembers(models.Model):
    """
    A company can be a member of a campaign
    """
    company = models.ForeignKey('companies.Company', related_name='campaigns')
    campaign = models.ForeignKey('campaigns.Campaign', related_name='members')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Joined campaign")
    updated_at = models.DateTimeField(auto_now=True)
    products = models.ManyToManyField('companies.Product')
    class Meta:
        unique_together = (('company', 'campaign'),)