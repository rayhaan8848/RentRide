from django.test import TestCase
from django.urls import reverse
from .models import User


class SignUpTests(TestCase):
    def signup_data(self, **overrides):
        data = {
            'fullname': 'Alex Example',
            'email': 'alex@example.com',
            'phone': '1234567890',
            'password': 'Long-Random-Password-948!',
            'cpassword': 'Long-Random-Password-948!',
        }
        data.update(overrides)
        return data

    def test_signup_creates_user_with_generated_username(self):
        response = self.client.post(reverse('signup'), self.signup_data())

        self.assertRedirects(
            response,
            f"{reverse('signup')}?tab=signup",
            fetch_redirect_response=False,
        )
        user = User.objects.get(email='alex@example.com')
        self.assertTrue(user.username)
        self.assertTrue(user.check_password('Long-Random-Password-948!'))

    def test_signup_rejects_duplicate_email(self):
        User.objects.create_user(
            username='existing-user',
            email='alex@example.com',
            password='Long-Random-Password-948!',
        )

        response = self.client.post(reverse('signup'), self.signup_data())

        self.assertRedirects(
            response,
            f"{reverse('signup')}?tab=signup",
            fetch_redirect_response=False,
        )
        self.assertEqual(User.objects.filter(email='alex@example.com').count(), 1)

    def test_signup_uses_available_username_when_email_name_is_taken(self):
        User.objects.create_user(
            username='alex',
            email='existing@example.com',
            password='Long-Random-Password-948!',
        )

        self.client.post(
            reverse('signup'),
            self.signup_data(email='alex@another.example'),
        )

        user = User.objects.get(email='alex@another.example')
        self.assertEqual(user.username, 'alex-1')
