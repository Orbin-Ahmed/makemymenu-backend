from django.contrib import admin
from . import models
from django.contrib.auth.models import Group

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    pass


class RegisterTokenAdmin(admin.ModelAdmin):
    pass


class PasswordTokenAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Registration_verification, RegisterTokenAdmin)
admin.site.register(models.Password_verification, PasswordTokenAdmin)
admin.site.unregister(Group)
