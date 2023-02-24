from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    #the primary key of a model which “extends” another model('Customer' model extends to 'User' Model)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    profile_pic = models.ImageField(default = 'profile_pic1', null = True, blank = True)
    def __str__(self):
        return self.name
        
class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    TYPE_OF_PRODUCT = (('Indoor', 'Indoor'), ('Outdoor', 'Outdoor'))
    name = models.CharField(max_length=200, null=True)
    category = models.CharField(max_length=200, null=True, choices=TYPE_OF_PRODUCT)
    price = models.FloatField(null=True)
    description = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = (('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Out for Delivery', 'Out for Delivery'), ('Delivered', 'Delivered'))
    customer_name = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product_name = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, choices=STATUS, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.status