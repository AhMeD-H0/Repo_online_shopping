from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from accounts.models import User


class AccountsTests(TestCase):
    def setUp(self):
        self.user_data = {
            "email": "test@example.com",
            "password": "strong_password123",
            "full_name": "Test User",
            "phone_number": "1234567890"
        }
        self.user = User.objects.create_user(
            email=self.user_data["email"],
            password=self.user_data["password"],
            full_name=self.user_data["full_name"],
            phone_number=self.user_data["phone_number"]
        )

    def test_user_login_valid(self):
        response = self.client.post(reverse('accounts:login'), {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, 302)  # Redirects after successful login
        self.assertRedirects(response, reverse('shop:home'))

    def test_user_login_invalid(self):
        response = self.client.post(reverse('accounts:login'), {
            'email': self.user_data['email'],
            'password': 'wrong_password'
        })
        self.assertEqual(response.status_code, 200)  # Stays on the login page
        self.assertContains(response, 'username or password is wrong')

    def test_register_user(self):
        response = self.client.post(reverse('accounts:register'), {
            'email': 'newuser@example.com',
            'password': 'new_password123',
            'full_name': 'New User',
            'phone_number': '0987654321'
        })
        self.assertEqual(response.status_code, 302)  # Redirects after successful registration
        self.assertRedirects(response, reverse('shop:home'))
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())
