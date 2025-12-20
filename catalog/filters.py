# myapp/filters.py
import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    # Add custom filters, e.g., using specific lookups
    price_gt = django_filters.NumberFilter(field_name="price", lookup_expr='gt') # greater than
    description_contains = django_filters.CharFilter(field_name="description", lookup_expr='contains')

    class Meta:
        model = Product
        # You can still use 'fields' for simple exact matches
        fields = ['category', 'price_gt', 'description_contains']
    
    