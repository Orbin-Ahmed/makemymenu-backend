from django.contrib import admin
from . import models
# Register your models here.


class CompanyAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Company, CompanyAdmin)
