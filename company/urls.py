from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register(r'api', CompanyView, basename='CRUD Company')

urlpatterns = [
    path('', include(router.urls)),
    path('transfer-owner/', ownership_transfer, name= "transfer Owner"),

]
