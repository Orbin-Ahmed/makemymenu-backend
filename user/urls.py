from django.urls import path, include
from drf_yasg.openapi import Contact
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register(r'api', UserView, basename='CRUD User')
router.register(r'faq', FAQView, basename='Contact Us')
router.register(r'create', ManagerCreateView, basename='Create Manager/Owner')


urlpatterns = [
    path('', include(router.urls)),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register-verify/', register_verify, name='Registration Verification'),
    path('info/', user_summary, name='User Summary'),
    path('reset/', reset_password, name='Reset Password'),
    path('tnc/', TnC, name='TNC'),
    path('about-us/', about_us, name='About Us'),
    path('feedback/', feedback, name='Feedback'),
    path('contact-us/', contact_us, name='Contact'),
    path('token/', user_token, name="get User Info by token"),
]
#https://django-rest-auth.readthedocs.io/en/latest/introduction.html