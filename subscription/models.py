from django.db import models

from branch.models import Branch
from company.models import Company
from makeMyMenuBackend.models import BaseModel
from datetime import timedelta, date


# Create your models here.


class Subscription(BaseModel, models.Model):
    branch = models.OneToOneField(Branch, on_delete=models.CASCADE, null=True)
    subscription_level = models.IntegerField(default=1)
    start_date = models.DateField(auto_now=True)
    end_date = models.DateField(editable=False)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    payment_id = models.CharField(max_length=100, blank=True, null=True)

    @staticmethod
    def get_default_end_date():
        return date.today() + timedelta(days=30)

    def save(self, *args, **kwargs):
        if not self.id:
            self.end_date = self.get_default_end_date()
        super().save(*args, **kwargs)



