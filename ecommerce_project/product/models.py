
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

RATING=(
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
)

class Category(models.Model):

    name = models.CharField(max_length = 50, unique = True)

class Product(models.Model):

     user_model = get_user_model() 

     name = models.CharField(max_length = 50)

     shopuser = models.ForeignKey(user_model, on_delete = models.CASCADE)

     category = models.ForeignKey(Category, on_delete = models.CASCADE)

     price = models.DecimalField(max_digits=10, decimal_places=2)

     brand = models.CharField(max_length = 50)

     color = models.CharField(max_length = 50)

     material = models.CharField(max_length = 50)

     published = models.BooleanField(default = False)

     description = models.CharField(max_length = 200, default='')

     rating = models.CharField(choices = RATING, max_length = 5, default = RATING[4])

"""
from product.models import Category,Product

c = Category.objects.get(id=1)

s = get_user_model().objects.get(id=40)

p = Product(name='iphone', price=50000, brand='apple', color='red', material ='plastic', published=True, description="greatest phone in the world")

"""
