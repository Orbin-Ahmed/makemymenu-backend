from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register(r'api', GroupView, basename='CRUD Group')

urlpatterns = [
    path('', include(router.urls)),
    path('multiple-update/', multiple_update, name='update multiple group'),
]
