from django.urls import path, include
from rest_framework import routers
from .views import (MenuView, get_menu, PrimaryMenuView, get_stat, counter, get_category_menu, get_primary,
                    multiple_update, item_suggestions)

router = routers.SimpleRouter()
router.register(r'api', MenuView, basename='CRUD Menu')
router.register(r'primary', PrimaryMenuView, basename='python Primary Menu')

urlpatterns = [
    path('', include(router.urls)),
    path('stats/', get_stat, name='stats'),
    path('get-primary/', get_primary, name='get primary menu'),
    path('counter/', counter, name='counter++'),
    path('get-menu/', get_menu, name='get menu'),
    path('get-category-menu/', get_category_menu, name='get category menu'),
    path('multiple-update/', multiple_update, name='update multiple menu'),
    path('item-ai/', item_suggestions, name='get item suggestions'),
]
