from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.forms.user_form import CustomSignupForm


User = get_user_model()

class CustomSignupFormTests(TestCase):

    def test_7_true_signup_new_account(self):
        """
        フォームからの新規登録の有効性確認
        """
        form_data = {
            'email': 'test@test.com',
            'password1': 'test0000',
            'password2': 'test0000'
        }
        form = CustomSignupForm(form_data)

        self.assertTrue(form.is_valid())


    def test_8_true_clean_email_method(self):
        """
        カスタマイズしたclean_emailメソッドを確認
        """
        test_email = 'test123@test.com'

        user = User(
            email=test_email,
            password='test0000',
        )
        user.save()

        form_data = {
            'email': test_email,
            'password1': 'test0000',
            'password2':'test0000'
        }
        form = CustomSignupForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('email', form.errors)
        self.assertEqual(
            form.errors['email'],
            ['このメールアドレスは既に登録されています。']
        )
