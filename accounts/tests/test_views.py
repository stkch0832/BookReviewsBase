from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from config import settings
from allauth.account.models import EmailAddress

User = get_user_model()
signup_url = reverse('accounts:accounts_signup')
login_url = reverse('accounts:accounts_login')
login_redirect_url = settings.LOGIN_REDIRECT_URL

class SignupViewTests(TestCase):
    def test_9_true_signup_view_get_method(self):
        """
        getメソッドにおいて、status_codeおよびtemplateの確認
        """
        response = self.client.get(signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/signup.html')

    def test_10_true_signup_view_post_method(self):
        """
        postメソッドにおいて、status_codeおよびtemplateの確認
        """
        form_data = {
            'email': 'test@test.com',
            'password1': 'test0000',
            'password2': 'test0000',
        }
        response = self.client.post(signup_url, data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/confirm-email/")

        response = self.client.get("/accounts/confirm-email/")
        self.assertTemplateUsed(response, 'account/verification_sent.html')


class LoginViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com",
            password="test0000"
        )

        email_address = EmailAddress.objects.create(
            user=self.user,
            email=self.user.email,
            verified=True,
            primary=True,
        )

    def test_11_true_login_view_get_method(self):
        """
        getメソッドにおいて、status_codeおよびtemplateの確認
        """
        response = self.client.get(login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_12_true_login_view_post_method(self):
        """
        postメソッドにおいて、status_codeおよびtemplateの確認
        """
        form_data = {
            'login': self.user.email,
            'password': 'test0000',
        }
        response = self.client.post(login_url, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, settings.LOGIN_REDIRECT_URL)
        response = self.client.get(settings.LOGIN_REDIRECT_URL)
        self.assertTemplateUsed(response, 'home.html')
