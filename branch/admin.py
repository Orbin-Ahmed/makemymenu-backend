from django.contrib import admin
from . import models


# Register your models here.


class BranchAdmin(admin.ModelAdmin):
    pass


# class LocalizationAdmin(admin.ModelAdmin):
#     pass
#
#
# class Notification_settings_Admin(admin.ModelAdmin):
#     pass
#
#
# class FormatAdmin(admin.ModelAdmin):
#     pass


admin.site.register(models.Branch, BranchAdmin)
# admin.site.register(models.Localization, LocalizationAdmin)
# admin.site.register(models.Notification_settings, Notification_settings_Admin)
# admin.site.register(models.Date_time_format, FormatAdmin)
