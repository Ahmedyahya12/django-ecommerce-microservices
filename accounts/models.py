from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.managers import CustomUserManager

# Create your models here.

class CustomUser(AbstractUser):
    """
    Custom user model.
    """
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)  # Use email as the unique identifier
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"  # Email used for authentication
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Required fields when creating a superuser

    # Make `username` field nullable as you do not use it for authentication
    # username = models.CharField(max_length=150, blank=True, null=True)  # Allow `username` to be nullable

    # Ensure the model uses the custom manager
    objects = CustomUserManager()

    def __str__(self):
        return self.email
