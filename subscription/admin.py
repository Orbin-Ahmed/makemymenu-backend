from django.contrib import admin
from . import models

# Register your models here.


class SubscriptionAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Subscription, SubscriptionAdmin)
