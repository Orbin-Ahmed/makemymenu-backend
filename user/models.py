from django.db import models
from django.contrib.auth.models import AbstractUser
from makeMyMenuBackend.models import BaseModel
from django.utils.translation import gettext_lazy as _


# Create your models here.


class User(AbstractUser, BaseModel):
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    email = models.EmailField(_("email address"), unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    nid = models.CharField(max_length=50, null=True, blank=True, unique=True, default=None)
    phone = models.CharField(max_length=11, null=True, blank=True)
    image = models.ImageField(upload_to='user/', null=True, blank=True)
    verified = models.BooleanField(default=False)

    def get_name(self):
        return f'{self.first_name} {self.last_name}'


class Registration_verification(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.IntegerField()


class Password_verification(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.IntegerField()


class FAQ(models.Model):
    faq_question = models.TextField()
    faq_answer = models.TextField()

# class ContactUs(models.Model):
#     subject = models.CharField(max_length=200)
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
