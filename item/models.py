from django.db import models
from branch.models import Branch
from makeMyMenuBackend.models import BaseModel


# Create your models here.


class Item(BaseModel, models.Model):
    branch = models.ManyToManyField(Branch)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    category = models.CharField(max_length=255)
    image = models.ImageField(upload_to='item/', null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    video_link = models.URLField(max_length=255, null=True, blank=True)
    barcode = models.CharField(max_length=255, null=True, blank=True, unique=True)
