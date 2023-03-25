from django.db import models
from branch.models import Branch
from item.models import Item
from makeMyMenuBackend.models import BaseModel


# Create your models here.


class Group(BaseModel, models.Model):
    branch = models.ManyToManyField(Branch)
    item = models.ManyToManyField(Item)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField()
    discount = models.FloatField(default=0)
    category = models.CharField(max_length=50)
    image = models.ImageField(upload_to='group/', null=True, blank=True)
    video_link = models.URLField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
