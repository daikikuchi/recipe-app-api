from django.test import TestCase
from django.contrib.auth import get_user_model
# get_user_model returns a user model that is currently active in project


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = "kikuchi.dai@gmail.com"
        password = "password"
        # print(get_user_model()) <class 'core.models.User'>
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is test_new_user_email_normalized"""
        email = 'test@GMAIL.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test Creating user with no email raises error
         what this does is anything that we run in here should
         raise the value error.
         And if it doesn't raise a value error then this test will fail.
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test Creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@gmail.com',
            'test123'
        )
        # is_superuser is included in PermissionsMixin
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)