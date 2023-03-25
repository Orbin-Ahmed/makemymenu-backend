from django.urls import path, include
from rest_framework import routers
from .views import SubscriptionViewSet, update_subscription

router = routers.SimpleRouter()
router.register(r'api', SubscriptionViewSet, basename='CRD Subscription')

urlpatterns = [
    path('', include(router.urls)),
    path('update/', update_subscription, name='update'),
]
