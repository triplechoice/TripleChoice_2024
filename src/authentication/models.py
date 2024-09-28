from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from triple_choice.db.mixins import AuthorMixin, TimeStampMixin


class UserManager(BaseUserManager):
    def create_superuser(self, username, email, password, company_name, phone):
        user = self.model(
            email=email,
            password=password,
            username=username,
            company_name=company_name,
            phone=phone
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        userprofile = UserProfile.objects.create(user=user)
        userprofile.save()
        return user


class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    company_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=25)
    REQUIRED_FIELDS = ['email', 'company_name', 'phone']

    objects = UserManager()

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    file = models.ImageField(upload_to='media', blank=True, null=True)

    billing_street = models.CharField(max_length=255, blank=True, null=True)
    billing_building = models.CharField(max_length=255, blank=True, null=True)
    billing_state = models.CharField(max_length=50, blank=True, null=True)
    billing_city = models.CharField(max_length=250, blank=True, null=True)
    billing_zip_code = models.CharField(max_length=50, blank=True, null=True)

    shipping_street = models.CharField(max_length=255, blank=True, null=True)
    shipping_building = models.CharField(max_length=255, blank=True, null=True)
    shipping_state = models.CharField(max_length=50, blank=True, null=True)
    shipping_city = models.CharField(max_length=250, blank=True, null=True)
    shipping_zip_code = models.CharField(max_length=50, blank=True, null=True)
