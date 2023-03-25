from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register(r'api', BranchView, basename='CRUD Branch')
router.register(r'zone', localizationView, basename='RU localization')
router.register(r'format', FormatView, basename='RU Date-Time-Format')
router.register(r'n-settings', Notification_settingsView, basename='RU localization')

urlpatterns = [
    path('', include(router.urls)),
    path('invite/', manager_invite, name="manager invite"),
    path('get-qr/', get_qr, name="get Menu/Wifi QR Code"),
]
