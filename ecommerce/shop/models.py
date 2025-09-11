from django.db import models
from django.contrib.auth.models import User

# Create your models here.
DIVISION_CHOICES = (
    ('Dhaka','Dhaka'),
    ('Rangpur','Rangpur'),
    ('Rajshahi','Rajshahi'),
    ('Khulna','Khulna'),
    ('Barishal','Barishal'),
    ('Chattogram','Chattogram'),
    ('Mymenshing','Mymenshing'),
    ('Sylhet','Sylhet'),
)

def user_directory_path(instance, filename):
    return f'user_{instance.user.id}/{filename}'

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to=user_directory_path, default='default.jpg')
    division = models.CharField(choices=DIVISION_CHOICES, max_length=50, null=True, blank=True)
    district = models.CharField(max_length=20)
    thana = models.CharField(max_length=50)
    street_address = models.CharField(max_length=200)
    zipcode = models.IntegerField(blank=True, null=True)
    contact = models.CharField(max_length = 20, blank=True, null=True)
    

    def __str__(self):
        return str(self.id)

# Category choices
CATEGORY_CHOICES = (
    ('tshirt', 'T-shirt'),
    ('pant', 'Pant'),
    ('jacket', 'Jacket'),
    ('hoodie', 'Hoodie'),
    ('watches', 'Watches'),
    ('bags', 'Bags'),
    ('belts', 'Belts'),
    ('sunglasses', 'Sunglasses'),
    ('sandals', 'Sandals'),
    ('boots', 'Boots'),
    ('loafers', 'Loafers'),
    ('sneakers', 'Sneakers'),
)

# Brand choices
BRAND_CHOICES = (
    ('nike', 'Nike'),
    ('adidas', 'Adidas'),
    ('puma', 'Puma'),
    ('zara', 'Zara'),
    ('hm', 'H&M'),
    ('gucci', 'Gucci'),
    ('prada', 'Prada'),
)


class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(choices=BRAND_CHOICES, max_length=50)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20)
    product_image = models.ImageField(upload_to='img/product', blank=True, null=True)

    # Multi-select via ManyToMany
    colors = models.ManyToManyField(Color, blank=True)
    sizes = models.ManyToManyField(Size, blank=True)

    additional_images = models.ManyToManyField(
        'ProductImage', blank=True, related_name='products'
    )

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='product_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.color} image for {self.product.title}" if self.color else f"Image for {self.product.title}"




class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)



STATUS_CHOICE = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the Way', 'On the Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICE, default='Pending')