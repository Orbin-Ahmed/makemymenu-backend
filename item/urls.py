from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'api', ItemView, basename='CRUD Item')

urlpatterns = [
    path('', include(router.urls)),
    path('multiple-update/', multiple_update, name='update multiple item'),
]
