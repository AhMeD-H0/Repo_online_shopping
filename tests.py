from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthenticationTests(TestCase):

    def setUp(self):
        # إعداد بيانات المستخدم المبدئية
        self.signup_url = reverse('signup')  # اسم مسار صفحة التسجيل
        self.login_url = reverse('login')  # اسم مسار صفحة تسجيل الدخول
        self.home_url = reverse('home')  # اسم مسار الصفحة الرئيسية
        self.user_data = {
            'username': 'TestUser',
            'email': 'testuser@example.com',
            'password': 'password123'
        }

    def test_signup(self):
        # اختبار وظيفة التسجيل
        response = self.client.post(self.signup_url, {
            'username': self.user_data['username'],
            'email': self.user_data['email'],
            'password1': self.user_data['password'],  # Django يستخدم password1 و password2
            'password2': self.user_data['password'],
        })
        self.assertEqual(response.status_code, 302)  # يفترض أن يعيد التوجيه إلى صفحة تسجيل الدخول
        self.assertTrue(User.objects.filter(email=self.user_data['email']).exists())
        user = User.objects.get(email=self.user_data['email'])
        self.assertEqual(user.username, self.user_data['username'])

    def test_login(self):
        # تسجيل المستخدم أولاً
        User.objects.create_user(
            username=self.user_data['username'],
            email=self.user_data['email'],
            password=self.user_data['password']
        )
        
        # اختبار وظيفة تسجيل الدخول
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],  # يمكن استخدام username أو email حسب إعداد المشروع
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, 302)  # يفترض أن يعيد التوجيه إلى الصفحة الرئيسية
        self.assertEqual(response.url, self.home_url)

    def test_invalid_login(self):
        # اختبار تسجيل الدخول باستخدام بيانات خاطئة
        response = self.client.post(self.login_url, {
            'username': 'wronguser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # يبقى في صفحة تسجيل الدخول
        self.assertContains(response, "Invalid username or password")  # تأكد من وجود الرسالة المناسبة
