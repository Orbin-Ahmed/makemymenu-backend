from django.db import models
from makeMyMenuBackend.models import BaseModel
from group.models import Group
from branch.models import Branch
from menu.models import Menu
from item.models import Item

# Create your models here.


class GroupOffers(BaseModel, models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=255)
    discount = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField(upload_to='MealOffers/', null=True, blank=True)


class BranchOffers(BaseModel, models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=255)
    discount = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField(upload_to='BranchOffers/', null=True, blank=True)


class MenuOffers(BaseModel, models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=255)
    discount = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField(upload_to='MenuOffers/', null=True, blank=True)


class ItemOffers(BaseModel, models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=255)
    discount = models.FloatField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    image = models.ImageField(upload_to='ItemOffers/', null=True, blank=True)
