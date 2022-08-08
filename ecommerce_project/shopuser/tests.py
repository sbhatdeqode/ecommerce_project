from django.test import TestCase
from django.test.client import Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.apps import apps

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


    def test_shop_uder_product_list(self):

        self.client.force_login(self.shopuser)

        response = self.client.get(reverse('shopuser_products'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shopuser_products.html')
        self.assertNotContains(response, 'Customer Portal')
        self.assertNotContains(response, 'Admin Portal')
        self.assertContains(response, 'Shopuser Portal')




