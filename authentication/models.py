from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("Users must have a valid email address")
        if not kwargs.get('username'):
            raise ValueError('You must have a valid username')
        account = self.model(email=self.normalize_email(email),
                             username=kwargs.get('username'))
        account.set_password(password)
        account.save()
        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)
        account.is_admin = True
        account.is_staff = True
        account.save()
        return account

class Account(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    profile_picture = models.ForeignKey('images.Image', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    tagline = models.CharField(max_length=140, blank=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    #followees => the people who this person is following
    followees = models.ManyToManyField('self', symmetrical=False, blank=True, null=True)
    liked_products = models.ManyToManyField('companies.Product', blank=True, null=True)
    liked_companies = models.ManyToManyField('companies.Company', blank=True, null=True)
    liked_causes = models.ManyToManyField('causes.Cause', blank=True, null=True)

    objects = AccountManager()
    USERNAME_FIELD = 'email'
    #we still want the users to give a username
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    def get_full_name(self):
        return " ".join([self.first_name, self.last_name])
    def get_short_name(self):
        return self.first_name
    def get_username(self):
        return self.username


