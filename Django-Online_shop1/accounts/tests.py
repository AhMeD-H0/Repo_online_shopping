from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthenticationTests(TestCase):

    def setUp(self):
        
        self.signup_url = reverse('Repo_online_shopping\Django-Online_shop1\accounts\templates\accounts\register.html')  
        self.login_url = reverse('Repo_online_shopping\Django-Online_shop1\accounts\templates\accounts\login.html')  
        self.home_url = reverse('Repo_online_shopping\Django-Online_shop1\shop\templates\shop\home.html')  
        self.user_data = {
            'username': 'TestUser',
            'email': 'testuser@example.com',
            'password': 'password123'
        }

    def test_signup(self):
        
        response = self.client.post(self.signup_url, {
            'username': self.user_data['username'],
            'email': self.user_data['email'],
            'password1': self.user_data['password'],  
            'password2': self.user_data['password'],
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(User.objects.filter(email=self.user_data['email']).exists())
        user = User.objects.get(email=self.user_data['email'])
        self.assertEqual(user.username, self.user_data['username'])

    def test_login(self):
        
        User.objects.create_user(
            username=self.user_data['username'],
            email=self.user_data['email'],
            password=self.user_data['password']
        )
        
        
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'], 
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(response.url, self.home_url)

    def test_invalid_login(self):
        
        response = self.client.post(self.login_url, {
            'username': 'wronguser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password")
