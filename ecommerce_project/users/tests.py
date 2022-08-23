"""
    users test module
"""
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from .forms import ShopuserAddForm
# Create your tests here.

class UsersTest(TestCase):

    """
        users test class
    """

    @classmethod
    def setUpTestData(cls):

        """
            Setup run.
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

    def test_shop_user_signup(self):

        """
            test shop user signup viw
        """

        response = self.client.get(reverse('account_shopuser_signup'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/shop_user_signup.html')


    def test_shopuser_list(self):

        """
            test shop user list viw
        """

        self.client.force_login(self.admin)

        response = self.client.get(reverse('shopuser_list_approval'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/shopuser_list.html')


    def test_shopuser_detail(self):

        """
            test shop user detail viw
        """

        response = self.client.get(reverse('shopuser_details', kwargs={'user_id':self.shopuser.id}))

        self.assertEqual(response.status_code, 302)


    def test_shopuser_update(self):

        """
            test shop user update viw
        """

        data = {'shop_type': 'electronics', 'shop_name':'croma'}

        response = self.client.get(reverse('update_shopuser', kwargs = {'pk':self.shopuser.id}))

        self.assertEqual(response.status_code, 302)

        self.client.force_login(self.admin)
        response = self.client.get(reverse('update_shopuser', kwargs = {'pk':self.shopuser.id}))

        response_post = self.client.post(
            reverse(
            'update_shopuser' ,
            kwargs = {'pk':self.shopuser.id,},
            ), data)

        self.assertEqual(response_post.status_code, 204)


    def test_shopuser_crud(self):

        """
            test shop user crud viw
        """

        self.client.force_login(self.admin)
        response = self.client.get(reverse('shopuser_crud',))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/shopuser_crud.html')


    def test_shopuser_delete(self):

        """
            test shop user delete viw
        """

        self.client.force_login(self.admin)

        response = self.client.get(reverse('delete_shopuser', kwargs = {'pk':self.shopuser.id}))

        self.assertEqual(response.status_code, 200)

        response_post = self.client.post(
            reverse(
            'delete_shopuser' ,
            kwargs = {'pk':self.shopuser.id,},
            ))

        self.assertEqual(response_post.status_code, 204)

    def test_shopuser_add(self):

        """
            test shop user add viw
        """

        shopuser_data = {
            'username':'test_user2', 'email':'test_user2@test.com',
            'user_type': '2'

        }

        self.client.force_login(self.admin)

        response = self.client.get(reverse('add_shopuser'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/shopuser_add.html')

        form = ShopuserAddForm(shopuser_data)

        self.assertFalse(form.is_valid())


    def test_shopuser_edit_profile(self):

        """
            test shop user edit viw
        """

        shopuser_data = {
            'username':'test_user3', 'email':'test_user3@test.com',

        }

        self.client.force_login(self.admin)

        response = self.client.get(reverse('edit_profile_shop', kwargs = {'pk':self.shopuser.id}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/profile_edit.html')

        response_post = self.client.post(
            reverse(
            'edit_profile_shop' ,
            kwargs = {'pk':self.shopuser.id,},
            ), shopuser_data)

        self.assertEqual(response_post.status_code, 200)


    def test_profile(self):

        """
            test profile viw
        """

        self.client.force_login(self.admin)

        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/profile.html')
