from django.db import models
from company.models import Company
from user.models import User
from makeMyMenuBackend.models import BaseModel


# Create your models here.


class Branch(BaseModel, models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    manager = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_default = models.BooleanField(default=False)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(unique=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    QR_counter = models.IntegerField(default=0)
    QR = models.ImageField(upload_to='MenuQR/', null=True, blank=True)
    Wifi = models.ImageField(upload_to='MenuQR/', null=True, blank=True)
    placeholder_item = models.CharField(max_length=255, null=True, blank=True)
    placeholder_meals = models.CharField(max_length=255, null=True, blank=True)


class Localization(BaseModel, models.Model):
    branch = models.OneToOneField(Branch, on_delete=models.CASCADE)
    country = models.CharField(max_length=255, default="Bangladesh")
    time_zone = models.CharField(max_length=255, default="UTC+06:00")
    currency = models.CharField(max_length=255, default="BDT")
    language = models.CharField(max_length=255, default="EN")


class Date_time_format(BaseModel, models.Model):
    branch = models.OneToOneField(Branch, on_delete=models.CASCADE)
    date_format = models.CharField(max_length=255, default="dd-mm-yyyy")
    currency_precision = models.CharField(max_length=50, default=3)
    time_format = models.CharField(max_length=255, default="hh:mm:ss")
    number_format = models.CharField(max_length=255, default="#,###.##")
    begin_week = models.CharField(max_length=255, default="Sunday")


class Notification_settings(BaseModel, models.Model):
    branch = models.OneToOneField(Branch, on_delete=models.CASCADE)
    system_update = models.BooleanField(default=False)
    change_log = models.BooleanField(default=False)
