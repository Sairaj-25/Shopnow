from django.db import models

from django.contrib.auth.models import User

from django.core.validators import RegexValidator

phone_validator = RegexValidator(regex=r'^\d{10}$', message="Phone number must be 10 digits")
pincode_validator = RegexValidator(regex=r'^\d{6}$', message="Pin Code must be 6 digits")
# Create your models here.

class Category(models.Model):
    CATEGORY_CHOICES = [
        ('fruits','Fruits'),
        ('vegetables','Vegetables'),
        ('dairy_products','Dairy Products'),
        ('groceries','Groceries'),
        ('snacks','Snacks'),
        ('medical','medical'),
    ]

    # name = models.CharField(max_length=100, unique = True, choices = CATEGORY_CHOICES, verbose_name="Category Name")

    name = models.CharField(max_length=100, unique = True, verbose_name="Category Name")
    def __str__(self):
        return self.name


# products
class Product(models.Model):
    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('g', 'Gram'),
        ('l', 'Liter'),
        ('ml', 'Milliliter'),
        ('piece', 'Piece'),
    ]

    name = models.CharField(max_length=200, verbose_name='Product Name')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='categories')  # on_delete=models.PROTECT
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Price')
    no_of_units = models.IntegerField(default=1)
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES, verbose_name='product unit', default='piece', null=True)
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name='Stock Quantity')
    is_active = models.BooleanField(default=True, verbose_name='Is Active')
    image = models.ImageField(upload_to='images/',verbose_name='Product Image')
    description = models.TextField(blank=True,null=True, verbose_name='Description')
    created_at = models.DateTimeField(auto_now=True,verbose_name='Created Time')
    updated_at = models.DateTimeField(auto_now=True, blank=True, null= True)

    @property
    def is_in_stock(self):
        return self.stock_quantity and self.stock_quantity > 0
    
    def __str__(self):
        return self.name
    
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(verbose_name='Email',default=user)
    phone = models.CharField(max_length=10,validators=[phone_validator], verbose_name = 'Phone Number')
    address = models.TextField(verbose_name='Address')
    landmark = models.CharField(max_length=200,blank=True,null=True)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    pin_code = models.CharField(max_length=6,validators=[pincode_validator])

    def __str__(self):
        return self.name  # Ensure this returns a string, not a User object
    


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_cart')
    quantity = models.PositiveIntegerField(null=False, blank=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Same product can't be added more than once to same user's cart
        unique_together = ('user', 'product')

    def get_total_price(self):
        return self.quantity * self.product.price
    
    def save(self, *args, **kwargs):
        if self.quantity < 1:  # Remove item if quantity is less than 1
            self.delete()
        else:
            super().save(*args, **kwargs)


class Order(models.Model):
    STATUS_CHOICES = [('Pending', 'Pending'),('On The Way', 'On The Way'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=255, unique=True)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_id} - {self.status}"


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity}) - Order {self.order.order_id}"
    
    def get_total_price(self):
        return self.quantity * self.product.price


# class Payment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     amount = models.IntegerField()
#     razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
#     razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
#     razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
#     paid=models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)