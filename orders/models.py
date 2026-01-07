from django.db import models
from django.conf import settings

from accounts.models import CustomerAddress
from catalog.models import Product


class OrderStatus(models.TextChoices):
    PROCESSING = 'Processing', 'Processing'
    SHIPPED = 'Shipped', 'Shipped'
    DELIVERED = 'Delivered', 'Delivered'
    CANCELLED = 'Cancelled', 'Cancelled'  


class PaymentStatus(models.TextChoices):
    PAID = 'Paid', 'Paid'
    UNPAID = 'Unpaid', 'Unpaid'


class PaymentMode(models.TextChoices):
    COD = 'COD', 'Cash on Delivery'                  
    CARD = 'CARD', 'Card Payment'           
    PAYPAL = 'PAYPAL', 'PayPal'        
    BANK_TRANSFER = 'BANK_TRANSFER', 'Bank Transfer' 
    APPLE_PAY = 'APPLE_PAY', 'Apple Pay'           
    GOOGLE_PAY = 'GOOGLE_PAY', 'Google Pay'          
    WALLET = 'WALLET', 'E-Wallet'                  
    CRYPTO = 'CRYPTO', 'Cryptocurrency'  
            

class Order(models.Model):

    customer=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,related_name='orders')
    address=models.ForeignKey(CustomerAddress,on_delete=models.SET_NULL,null=True)
    customer_name = models.CharField(max_length=100, blank=True, null=True)
    customer_email = models.EmailField(blank=True, null=True)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)
    shipping_street = models.CharField(max_length=100, blank=True, null=True)
    shipping_city = models.CharField(max_length=50, blank=True, null=True)
    shipping_state = models.CharField(max_length=50, blank=True, null=True)
    shipping_zip_code = models.CharField(max_length=20, blank=True, null=True)
    
     
    payment_reference = models.CharField(
        max_length=255, blank=True, null=True
    )
    payment_status=models.CharField(
         max_length=100,
         choices=PaymentStatus.choices,
         default=PaymentStatus.PAID)
    payment_mode=models.CharField(
         max_length=100,
         choices=PaymentMode.choices,
         default=PaymentMode.COD
     )
    order_status=models.CharField(
         max_length=100,
         choices=OrderStatus.choices,
         default=OrderStatus.PROCESSING
     )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.payment_reference}--{self.order_status}'


class OrderItem(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_items')
    product=models.ForeignKey(Product, null=True, on_delete=models.CASCADE, related_name='order_items')
    quantity=models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0) 


    def __str__(self):
        return f"{self.name} (x{self.quantity}) - {self.order}"