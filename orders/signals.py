from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from orders.models import OrderItem

@receiver(pre_save, sender=OrderItem)
def update_stock_on_order(sender, instance, **kwargs):
    product = instance.product

    if instance.pk:  # Update d'un OrderItem existant
        old_instance = OrderItem.objects.get(pk=instance.pk)
        diff = instance.quantity - old_instance.quantity
        product.stock -= diff
    else:  # Création
        product.stock -= instance.quantity

    product.save()

@receiver(post_delete, sender=OrderItem)
def update_stock_on_delete(sender, instance, **kwargs):
    product = instance.product
    product.stock += instance.quantity
    product.save()
