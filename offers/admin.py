from django.contrib import admin
from . import models


# Register your models here.


class GroupOfferAdmin(admin.ModelAdmin):
    pass


class BranchOfferAdmin(admin.ModelAdmin):
    pass


class ItemOfferAdmin(admin.ModelAdmin):
    pass


class MenuOfferAdmin(admin.ModelAdmin):
    pass


# admin.site.register(models.BranchOffers, BranchOfferAdmin)
# admin.site.register(models.GroupOffers, GroupOfferAdmin)
# admin.site.register(models.ItemOffers, ItemOfferAdmin)
# admin.site.register(models.MenuOffers, MenuOfferAdmin)
