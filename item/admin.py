from django.contrib import admin
from . import models


# Register your models here.

class ItemAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Item, ItemAdmin)
