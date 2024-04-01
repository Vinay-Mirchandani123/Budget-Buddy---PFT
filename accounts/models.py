from django.db import models
from django.contrib.auth.models import AbstractUser
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
from base.emails import account_activation_email
from .managers import UserManager
import uuid


# Create your models here.


# class Profile(BaseModel):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
#     email_verified = models.BooleanField(default=False)
#     email_token = models.CharField(max_length=100, blank=True, null=True)
#     # profile_image = models.ImageField(upload_to='profile')


# @receiver(post_save, sender=User)
# def send_email_token(sender, instance, created, **kwargs):
#     try:
#         if created:
#             email_token = str(uuid.uuid4())
#             Profile.objects.create(user = instance , email_token = email_token)
#             email = instance.email
#             account_activation_email(email, email_token)
#     except Exception as e:
#         print(e)

class User(AbstractUser):
    phone_number=models.CharField(max_length=12, unique=True)
    # phone_verified=models.BooleanField(default=False)
    # otp=models.CharField(max_length=6)
    REQUIRED_FIELDS=['phone_number']
    objects= UserManager()

class Editprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profileimage= models.ImageField(upload_to='userimage/', default='profile3.jpeg')
    namefirst= models.CharField(max_length=100, blank=False, null=False)
    lastname= models.CharField(max_length=100, blank=False, null=False)
    about= models.TextField(blank=False, null=False)
    job= models.CharField(max_length=100,blank=False, null=False)
    country= models.CharField(max_length=100, blank=False, null=False)
    address= models.TextField(blank=False, null=False)
    phone= models.CharField(max_length=12, blank=False, null=False)
    email= models.EmailField(blank=False, null=False)
    twitter= models.URLField(max_length=200, blank=True, null=True)
    facebook= models.URLField(max_length=200, blank=True, null=True)
    instagram= models.URLField(max_length=200, blank=True, null=True)
    linkedin= models.URLField(max_length=200, blank=True, null=True)
    