from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.deletion import CASCADE

# Create your models here.
STATE_CHOICES = (
    ('Hyderabad','Hyderabad'),
    ('Karachi','Karachi'),
    ('Lahore','Lahore'),
    ('Islamabad','Islamabad'),
    ('Multan','Multan'),
    ('Bihar','Bihar'),
    ('Vihari','Vihari'),
    ('Khanewal','Khanewal'),
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    locality = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=30)

    def __str__(self):
        return str(self.id)
    
CATEGORY_CHOICES = (
    ('M','Mobile'),
    ('L','Laptop'),
    ('TW','Top Wear'),
    ('BW','Bottom Wear'),
)

class Product(models.Model):
    title = models.CharField(max_length=30)
    selling_price = models.FloatField()
    discount_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=30)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='productimg') 

    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_price(self):
        return self.product.discount_price*self.quantity

STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the Way','On the Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
)

class Order_Place(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=30, default='Pending')
    def __str__(self):
        return str(self.id) 
    
    @property
    def total_price(self):
        return self.product.discount_price*self.quantity