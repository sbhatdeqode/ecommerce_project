"""
       Adminops test module
"""
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminopsTest(TestCase):

    """
       Adminops test class
    """

    @classmethod
    def setUpTestData(cls):

        """
            setup run
        """

        cls.client = Client()
        admin = get_user_model().objects.create(username='test_user1', email='test_user1@test.com')
        admin.user_type = '1'
        admin.is_admin = True
        admin.save()

        cls.admin = admin

        shopuser = get_user_model().objects.create(
            username='test_user2', email='test_user2@test.com'
            )
        shopuser.user_type = '2'
        shopuser.is_active = True
        shopuser.save()

        cls.shopuser = shopuser


        customer = get_user_model().objects.create(
            username='test_user3', email='test_user3@test.com'
            )
        customer.user_type = '2'
        customer.is_active = True
        customer.save()

        cls.customer = customer


    def test_adminops_home(self):

        """
            adminops_home view test
        """

        self.client.force_login(self.admin)

        response = self.client.get(reverse('adminops_home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adminops_home.html')
