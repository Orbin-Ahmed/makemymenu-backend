from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register(r'branch-offers', BranchOffersView, basename='CRUD BranchOffer')
router.register(r'menu-offers', MenuOffersView, basename='CRUD MenuOffer')
router.register(r'group-offers', GroupOffersView, basename='CRUD GroupOffer')
router.register(r'item-offers', ItemOffersView, basename='CRUD ItemOffer')


urlpatterns = [
    path('', include(router.urls)),
]
