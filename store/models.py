from cloudinary_storage.storage import MediaCloudinaryStorage
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.text import slugify

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address1 = models.CharField(max_length=255, blank=True, null=True)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    old_cart = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return self.user.username
    
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
       
       
# Automate the profile thing       
post_save.connect(create_user_profile, sender=User)


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, blank=True, null=True)
    price = models.DecimalField(default=0.00, max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    stock_quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='uploads/product/', blank=True, null=True, storage=MediaCloudinaryStorage())
    is_on_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0.00, max_digits=6, decimal_places=2)
    #id = models.AutoField(primary_key=True) -- is created automatically by Django

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(default=datetime.datetime.now)
    address = models.CharField(max_length=255, default='', blank=True)
    phone = models.CharField(max_length=15, default='', blank=True)
    status = models.BooleanField(default=False)


    def __str__(self):
        return self.product.name