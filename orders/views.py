from django.shortcuts import render
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from accounts.models import CustomerAddress
from catalog.models import Product
from common.user_account import User
from orders.models import Order, OrderItem, OrderStatus
from orders.serializers import OrderSerializer
from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def get_my_orders(request):
    user_email=request.data['email']
    user=get_object_or_404(User,email=user_email)
    orders =Order.objects.filter(customer=user)
    serializer=OrderSerializer(orders ,many=True)
    return Response(serializer.data)



@api_view(['DELETE'])
def cancel_order(request,pk):
    order=get_object_or_404(Order,id=pk)
    if order.order_status != OrderStatus.CANCELLED:
         order_items=order.order_items.all()
         for item in order_items:
              item.product.stock += item.quantity
              item.product.save()
          
    order.order_status=OrderStatus.CANCELLED
    order.save()
    serializer=OrderSerializer(order)
    return Response({'order':serializer.data,'message':'Your order  annulled successfully'})


@api_view(['POST'])
def add_order(request):
    data = request.data
    order_items = data.get('orderItems', [])

    # Vérifier si des produits sont envoyés
    if not order_items:
        return Response({'error': 'No order items received'}, status=400)

    # Récupérer l'utilisateur et son adresse
    user = get_object_or_404(User, email=data['email'])
    address = get_object_or_404(CustomerAddress, user=user)
    
    try:
        with transaction.atomic():
            # Création de la commande
            order = Order.objects.create(
                customer=user,
                address=address,

                # Infos client copiées
                customer_name=f"{user.first_name} {user.last_name}",
                customer_email=user.email,
                customer_phone=address.phone_no,

                # Infos livraison copiées
                shipping_street=address.street,
                shipping_city=address.city,
                shipping_state=address.state,
                shipping_zip_code=address.zip_code,

                total_amount=0  # initialisation
            )

            # Ajout des items de commande
            total_amount = 0
            for item in order_items:
                product = get_object_or_404(Product, id=item['product'])

                # Vérifier stock
                if product.stock < item['quantity']:
                    raise ValueError(f"Stock not sufficient for {product.name}")
                
                # Calcul montant
                item_total = product.price * item['quantity']

                # Créer l'item
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=product.price
                )

                # Mettre à jour le stock
                # product.stock -= item['quantity']
                product.save()

                # Ajouter au total
                total_amount += item_total

            # Mettre à jour le total de la commande
            order.total_amount = total_amount
            order.save()

            # Retourner la commande
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=201)

    except ValueError as e:
        return Response({'error': str(e)}, status=400)

    except Exception as e:
        return Response({'error': 'Something went wrong', 'details': str(e)}, status=500)

     


    