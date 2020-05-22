from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@londonappdev.com',
            password='password123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@londonappdev.com',
            password='password123',
            name='Test User Full Name',
        )

    def test_users_listed(self):
        """Test that users are listed on the user page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)



#
#
# from django.test import TestCase, Client
# # Client allows us to make test requests to our application in our unit tests
# from django.contrib.auth import get_user_model
# from django.urls import reverse
#
#
# class AdminSiteTests(TestCase):
#
#     def setUp(self):
#         self.client = Client()
#         self.admin_user = get_user_model().objects.create_superuser(
#             email='admin@gmail.com',
#             password='password'
#         )
#         # force_login() method to simulate the effect of a user
#         # logging into the site
#         self.client.force_login(self.admin_user)
#         self.user = get_user_model().objects.create_user(
#             email='test@gmail.com',
#             password='password',
#             name='Test user full name'
#         )
#
#     def test_users_listed(self):
#         """Test that users are listd on user page"""
#         url = reverse('admin:core_user_changelist')
#         # test client perform a HTTP GET on the url
#         res = self.client.get(url)
#
#         # assertContains checks the http res is 200
#         self.assertContains(res, self.user.name)
#         self.assertContains(res, self.user.email)
