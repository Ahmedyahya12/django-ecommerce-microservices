from django.db import models

# Category model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.name


# Product model
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='product_photos/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    stock = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
