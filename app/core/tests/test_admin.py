from django.test import TestCase, Client
# Client allows us to make test requests to our application in our unit tests
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@gmail.com',
            password='password'
        )
        # force_login() method to simulate the effect of a user
        # logging into the site
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='password',
            name='Test user full name'
        )

    def test_users_listed(self):
        """Test that users are listd on user page"""
        url = reverse('admin:core_user_changelist')
        # print('url',url) /admin/core/user/
        # test client perform a HTTP GET on the url
        res = self.client.get(url)
        # print('res',res)
        # <TemplateResponse status_code=200, "text/html; charset=utf-8">

        # assertContains checks the http res is 200
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        # /admin/core/user/1
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:core_user_add')

        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
