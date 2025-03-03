from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('User', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='User')
    is_verified = models.BooleanField(default=False)  # OTP verification
    otp = models.CharField(max_length=6, blank=True, null=True)  # Store OTP code

