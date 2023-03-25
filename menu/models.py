from datetime import datetime
from django.db import models
from item.models import Item
from makeMyMenuBackend.models import BaseModel
from branch.models import Branch
from group.models import Group


# Create your models here.

class Menu(BaseModel, models.Model):
    branch = models.ManyToManyField(Branch)
    item = models.ManyToManyField(Item)
    group = models.ManyToManyField(Group)
    name = models.CharField(max_length=255)
    # is_primary = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    QR_counter = models.IntegerField(default=0)
    status = models.CharField(max_length=255, default="Available")
    image = models.ImageField(upload_to='menu/', null=True, blank=True)
    video_link = models.URLField(max_length=255, null=True, blank=True)


class PrimaryMenu(BaseModel, models.Model):
    branch = models.OneToOneField(Branch, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.SET_NULL, null=True, blank=True)
    promo_image = models.ImageField(upload_to='promo/', null=True, blank=True)
    promo_name = models.CharField(max_length=255, null=True, blank=True)
    promo_vid = models.URLField(null=True, blank=True)


class MenuStat(BaseModel, models.Model):
    class Meta:
        unique_together = ('branch_id', 'company_id', 'date')

    # menu_id = models.IntegerField(null=True, blank=True)
    branch_id = models.IntegerField()
    company_id = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    total = models.IntegerField(default=0)
