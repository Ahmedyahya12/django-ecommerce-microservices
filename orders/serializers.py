from rest_framework import  serializers
from accounts.serializers import UserSerializer
from accounts.models import CustomerAddress
from orders.models import Order, OrderItem

class CustomerAddressSerializer(serializers.ModelSerializer):
      class Meta:
           model=CustomerAddress
           fields = [
            "id",
            "street",
            "city",
            "state",
            "zip_code",
            "phone_no",
        ]

class OrderItemSerializer(serializers.ModelSerializer):
      
      class Meta:
           model=OrderItem
           fields='__all__'

class OrderSerializer(serializers.ModelSerializer):
    order_items=OrderItemSerializer(many=True,read_only=True,)
    address = CustomerAddressSerializer(read_only=True)
    customer = UserSerializer(read_only=True)

    
    class Meta:
        model = Order
        fields = [
            "id",
             "order_items",
            "customer",
            "address",
            "customer_name",
            "customer_email",
            "customer_phone",
            "shipping_street",
            "shipping_city",
            "shipping_state",
            "shipping_zip_code",
            "payment_reference",
            "payment_status",
            "payment_mode",
            "order_status",
            "total_amount",
            "created_at",
            "updated_at",
           
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
            "payment_reference": {"write_only": True},  # يظهرش في GET
            "customer_email": {"required": True},       # لازم يكون موجود
        }