from django.contrib import admin

from catalog.models import Category, Product

# Register your models here.


admin.site.register([Product,Category])