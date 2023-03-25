from django.db import models
from makeMyMenuBackend.models import BaseModel
from user.models import User
from django.utils.translation import gettext_lazy as _


# Create your models here.


class Company(BaseModel, models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='company/', null=True, blank=True)
    # address = models.CharField(max_length=255)
    # phone_no = models.CharField(max_length=50, null=True, blank=True)
    # email = models.EmailField(_("email address"), unique=True)
    trade_license = models.CharField(max_length=50, unique=True, null=True, blank=True)
    type = models.CharField(max_length=255)
    type_status = models.BooleanField()


class TransferModel(BaseModel, models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    new_email = models.EmailField()
    