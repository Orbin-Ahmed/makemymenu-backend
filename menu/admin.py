from django.contrib import admin
from . import models


# Register your models here.


class MenuAdmin(admin.ModelAdmin):
    pass


class PrimaryMenuAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Menu, MenuAdmin)
admin.site.register(models.PrimaryMenu, PrimaryMenuAdmin)
