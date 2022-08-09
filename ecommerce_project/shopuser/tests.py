from django.test import TestCase
from django.test.client import Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.apps import apps

from .forms import ProductAddForm

# Create your tests here.

class ShopUserTest(TestCase):

    """
        Product List test class
    """
    
    @classmethod
    def setUpTestData(cls):

        # Setup run.

        Product = apps.get_model('product', 'Product')
        ProductAttribute = apps.get_model('product', 'ProductAttribute')
        Brand = apps.get_model('product', 'Brand')
        Category = apps.get_model('product', 'Category')
        Color = apps.get_model('product', 'Color')
        Material = apps.get_model('product', 'Material')
        Order = apps.get_model('product', 'Order')
        ProductSalesBrand = apps.get_model('product', 'ProductSalesBrand')
        ProductSalesCat = apps.get_model('product', 'ProductSalesCat')

        cls.client = Client()
        shopuser = get_user_model().objects.create(username='test_user1', email='test_user1@test.com')
        shopuser.user_type = '2'
        shopuser.is_active = True
        shopuser.save()

        cls.shopuser = shopuser

        cat = Category.objects.create(title = 'phones')
        cat.save()
        cls.cat = cat

        color = Color.objects.create(title = 'red')
        color.save()
        cls.color = color

        mat = Material.objects.create(title = 'plastic')
        mat.save()
        cls.mat = mat

        brand = Brand.objects.create(title = 'iphone')
        brand.save()
        cls.brand = brand

        product = Product.objects.create(
            title = 'iphone', shopuser = shopuser,
            category = cat, brand = brand,
            )

        product.save()
        cls.product = product

        p_at = ProductAttribute.objects.create(
            product = product, color = color,
            material = mat, price = 5000
            )

        p_at.save()

        cls.p_at = p_at


    def test_shop_user_product_list(self):

        self.client.force_login(self.shopuser)

        response = self.client.get(reverse('shopuser_products'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shopuser_products.html')
        self.assertNotContains(response, 'Customer Portal')
        self.assertNotContains(response, 'Admin Portal')
        self.assertContains(response, 'Shopuser Portal')


    def test_shop_user_product_publish_unpublish(self):

        self.client.force_login(self.shopuser)

        response = self.client.get(reverse('publish_unpublish'),{'product_id': self.product.id})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ajax/shopuser_products.html')
        self.assertNotContains(response, 'Admin Portal')
        self.assertNotContains(response, 'Customer Portal')

    def test_shop_user_product_publish_unpublish(self):

        self.client.force_login(self.shopuser)

        response = self.client.get(reverse('publish_unpublish'),{'product_id': self.product.id})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ajax/shopuser_products.html')
        self.assertNotContains(response, 'Admin Portal')
        self.assertNotContains(response, 'Customer Portal')


    def test_shop_user_product_delete(self):

        self.client.force_login(self.shopuser)

        response = self.client.get(reverse('product_delete'),{'product_id': self.product.id})
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ajax/shopuser_products.html')
        self.assertNotContains(response, 'Admin Portal')
        self.assertNotContains(response, 'Customer Portal')


    def test_shop_user_product_add(self):

        form_data = {
            'brand': self.brand.id, 
            'category': self.cat.id,
            'title':self.product.title,
            'detail':self.product.detail,
            'rating':5,
            'material':self.mat.id,
            'color':self.color.id,
            'price':self.p_at.price,
            'image':'4.jag',
            }

        form_pro_data = {
            'brand': 100, 
            'category': self.cat.id,
            'title':self.product.title,
            'detail':self.product.detail,
        }

        form_pro = ProductAddForm(form_pro_data)

        self.assertFalse(form_pro.is_valid())

        self.client.force_login(self.shopuser)

        response = self.client.get(reverse('product_add'),)

        response_post = self.client.post(reverse('product_add'), form_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_add.html')

        self.assertEqual(response_post.status_code, 200)
        self.assertTemplateUsed(response_post, 'product_update_success.html')


    def test_shop_user_product_update(self):

        form_data = {
            'p_id': self.product.id,
            'shopuser':self.shopuser,
            'brand': self.brand.id, 
            'category': self.cat.id,
            'title':self.product.title,
            'detail':self.product.detail,
            'rating':5,
            'material':self.mat.id,
            'color':self.color.id,
            'price':self.p_at.price,
            'image':'4.jpg',
            }

        self.client.force_login(self.shopuser)

        response = self.client.get(reverse('product_update'), {'p_id': self.product.id})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_update.html')

        response_post = self.client.post(reverse('product_update'), form_data,)

        self.assertEqual(response_post.status_code, 200)
        self.assertContains(response_post, "This field is required")


    def test_shop_user_order_list(self):

        self.client.force_login(self.shopuser)

        response = self.client.get(reverse('shopuser_order_list'),)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shopuser_orders.html')


    def test_shop_user_order_percentage(self):

        self.client.force_login(self.shopuser)

        response = self.client.get(reverse('shopuser_order_percentage'),)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shopuser_order_percetage.html')

