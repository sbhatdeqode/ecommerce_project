"""
    product models
"""

from django.utils.html import mark_safe
from django.db import models
from django.contrib.auth import get_user_model


RATING=(
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
)


class Category(models.Model):

    """
        Category Model
    """

    title = models.CharField(max_length = 100)

    class Meta:
        verbose_name_plural = '1. Categories'

    def __str__(self):
        return self.title


# Brand
class Brand(models.Model):

    """
        Brand Model
    """

    title = models.CharField(max_length = 100)

    class Meta:
        verbose_name_plural = '2. Brands'

    def __str__(self):
        return self.title


# Color
class Color(models.Model):

    """
        Color Model
    """

    title = models.CharField(max_length = 100)
    color_code = models.CharField(max_length = 100)

    class Meta:
        verbose_name_plural = '3. Colors'

    def color_bg(self):
        return mark_safe( f'<div style="width:30px; height:30px; background-color:{self.color_code}"></div>' )

    def __str__(self):
        return self.title


# Material
class Material(models.Model):

    """
        Material Model
    """

    title = models.CharField(max_length = 100)

    class Meta:
        verbose_name_plural = '4. Materials'

    def __str__(self):
        return self.title


# Product
class Product(models.Model):

    """
        Product Model
    """

    user_model = get_user_model() 

    title = models.CharField(max_length = 200)
    shopuser = models.ForeignKey(user_model, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete = models.CASCADE)
    published = models.BooleanField(default = False)
    detail = models.TextField()

    class Meta:
        verbose_name_plural = '5. Products'

    def __str__(self):
        return self.title


#attributes
class ProductAttribute(models.Model):

    """
        ProductAttribute Model
    """

    product = models.ForeignKey(Product,on_delete = models.CASCADE)
    color = models.ForeignKey(Color,on_delete = models.CASCADE)
    material = models.ForeignKey(Material,on_delete = models.CASCADE)
    price = models.PositiveIntegerField(default = 0)
    rating = models.CharField(choices = RATING, max_length = 5, default = RATING[4])
    image = models.ImageField(upload_to="product_imgs/", null = True)

    class Meta:
        verbose_name_plural = '6. ProductAttributes'

    def __str__(self):
        return self.product.title

    def image_tag(self):
        return mark_safe(f'<img src = {self.image.url} width = "40" height = "40" />')


# Cart
class Cart(models.Model):

    """
        Cart Model
    """

    user = get_user_model()

    customer = models.ForeignKey(user, on_delete = models.CASCADE)
    product = models.ForeignKey(Product,on_delete = models.CASCADE)

    class Meta:
        verbose_name_plural = '7. Carts'


# Wishlist
class Wishlist(models.Model):

    """
        Wishlist Model
    """

    user = get_user_model()

    customer = models.ForeignKey(user, on_delete = models.CASCADE)
    product = models.ForeignKey(Product,on_delete = models.CASCADE)


    class Meta:
        verbose_name_plural = '8. Wishlists'

# Order
class Order(models.Model):

    """
        order Model
    """

    user = get_user_model()

    customer = models.ForeignKey(user, on_delete = models.CASCADE)
    products = models.ManyToManyField(Product)
    paid = models.BooleanField(default = True)
    cancelled =  models.BooleanField(default = False)
    total_amount = models.BigIntegerField(default=0)

    class Meta:
        verbose_name_plural = '9. Orders'
