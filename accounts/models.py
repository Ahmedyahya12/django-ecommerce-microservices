from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.managers import CustomUserManager
from ecommerce_core import settings

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



    

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    discount_type = models.CharField(max_length=10, choices=(('percent','Percent'),('fixed','Fixed')), default='percent')
    expire_date = models.DateField(null=True,blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    usage_limit = models.PositiveIntegerField(default=1)
    used_count=models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
         return f'{self.code}--{self.discount_type}'
    

class CustomerAddress(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='addresses')
    street = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    state = models.CharField(max_length=100 ,null=True,blank=True)
    zip_code = models.CharField(max_length=20 ,null=True,blank=True)
    phone_no = models.CharField(max_length=20 ,null=True,blank=True)


