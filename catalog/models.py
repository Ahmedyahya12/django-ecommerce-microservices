from django.db import models
from django.utils.text import slugify


# Category model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    image = models.ImageField(upload_to="category_images/", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# Product model
class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    name = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to="product_photos/", blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    stock = models.PositiveIntegerField(
        default=0,
    )

    description = models.TextField(blank=True, null=True)
    available = models.BooleanField(
        default=True,
    )

    def save(self, *args, **kwargs):
        # 1. Add custom logic here (before saving to the database)
        if not self.slug:
            unique_slug = self.name
            counter = 1
            if Product.objects.filter(slug=unique_slug):
                unique_slug = slugify(f"{unique_slug}_${counter}")
                counter += 1
            unique_slug = slugify(f"{unique_slug}_${counter}")
            self.slug = unique_slug

        # 2. Call the parent class's save method to perform the actual database operation
        super(Product, self).save(*args, **kwargs)

        # 3. Add custom logic here (after saving to the database)

    def __str__(self):
        return f"{self.name} # {self.id}"
