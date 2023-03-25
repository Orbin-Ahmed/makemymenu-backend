from django.contrib import admin
from .models import Group


# Register your models here.
class MealAdmin(admin.ModelAdmin):
    pass


admin.site.register(Group, MealAdmin)
