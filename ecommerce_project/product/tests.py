"""
    Product test module
"""

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Product, Material, Category, Color, Brand, ProductAttribute, Order

# Create your tests here.
# pylint: disable=E1101

class ProductTest(TestCase):

    """
        Product List test class
    """

    @classmethod
    def setUpTestData(cls):

        """
            Setup run.
        """

        cls.client = Client()
        customer = get_user_model().objects.create(
            username='test_user1', email='test_user1@test.com'
            )
        customer.user_type = '3'
        customer.save()

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
            title = 'iphone', shopuser = customer,
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

        cls.customer = customer


    def test_product_list(self):

        """
            test product list viw
        """

        self.client.force_login(self.customer)

        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'productx_list.html')
        self.assertContains(response, 'Customer Portal')
        self.assertNotContains(response, 'Admin Portal')
        self.assertNotContains(response, 'Shopuser Portal')


    def test_product_search(self):

        """
            test product search viw
        """

        self.client.force_login(self.customer)

        response = self.client.get(reverse('product_search'),{'q': self.product.title})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')
        self.assertContains(response, 'Customer Portal')
        self.assertNotContains(response, 'Admin Portal')
        self.assertNotContains(response, 'Shopuser Portal')


    def test_product_filter(self):

        """
            test product filter viw
        """

        self.client.force_login(self.customer)

        response = self.client.get(reverse('product_filter'), {'mat':self.mat.id})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ajax/productx_list.html')


    def test_add_cart(self):

        """
            test add to cart viw
        """

        self.client.force_login(self.customer)

        response = self.client.get(reverse('add_to_cart'), {'product_id':self.product.id})

        self.assertEqual(response.status_code, 200)

        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"totalitems": 1, "message": "Item added to cart"}
        )


    def test_cart_list(self):

        """
            test cart list viw
        """

        self.client.force_login(self.customer)

        response = self.client.get(reverse('cart_list'),)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart.html')


    def test_cart_delete(self):

        """
            test cart delete viw
        """

        self.client.force_login(self.customer)

        response = self.client.get(reverse('delete_from_cart'), {'product_id':self.product.id})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ajax/cart.html')


    def test_add_wishlist(self):

        """
            test add to wishlist viw
        """

        self.client.force_login(self.customer)

        response = self.client.get(reverse('add_to_wishlist'), {'product_id':self.product.id})

        self.assertEqual(response.status_code, 200)

        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"totalitems": 1, "message": "Item is added to wishlist"}
        )


    def test_wishlist_list(self):

        """
            test  wishlist viw
        """

        self.client.force_login(self.customer)

        response = self.client.get(reverse('wishlist_list'),)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wishlist.html')


    def test_wishlist_delete(self):

        """
            test  wishlist delete viw
        """

        self.client.force_login(self.customer)

        response = self.client.get(reverse('delete_from_wishlist'), {'product_id':self.product.id})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ajax/wishlist.html')


    def test_place_order(self):

        """
            test place order viw
        """

        self.client.force_login(self.customer)

        response = self.client.get(reverse('place_order'),)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order.html')


    def test_buy_now(self):

        """
            test buy now viw
        """

        self.client.force_login(self.customer)

        response = self.client.get(reverse('buy_now'), {'pid':self.product.id})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order.html')


    def test_order_list(self):

        """
            test order list viw
        """

        self.client.force_login(self.customer)

        response = self.client.get(reverse('order_list'),)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order_list.html')


    def test_order_cancel(self):

        """
            test order cancel viw
        """

        self.client.force_login(self.customer)

        order = Order.objects.create(customer = self.customer)
        order.save()

        response = self.client.get(reverse('order_cancel'),{'order_id':order.id})

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'order_list.html')


    def test_product_detail(self):

        """
            test product detail viw
        """

        self.client.force_login(self.customer)

        response = self.client.get(reverse('product_detail'),{'p_id':self.product.id})

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'product_detail.html')

        self.assertContains(response, self.product.title)
