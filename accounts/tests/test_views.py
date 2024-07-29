from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models.profile_models import Profile
from config import settings
from allauth.account.models import EmailAddress
from datetime import date, timedelta
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from django.contrib.messages import get_messages


User = get_user_model()
signup_url = reverse('accounts:accounts_signup')
login_url = reverse('accounts:accounts_login')
login_redirect_url = settings.LOGIN_REDIRECT_URL

profile_detail_url = reverse('accounts:profile_detail')
profile_update_url = reverse('accounts:profile_edit')


class SignupViewTests(TestCase):
    def test_9_signup_view_get_method(self):
        """
        getメソッドにおいて、status_codeおよびtemplateの確認
        """
        response = self.client.get(signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/signup.html')

    def test_10_signup_view_post_method(self):
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
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="test@test.com",
            password="test0000"
        )

        email_address = EmailAddress.objects.create(
            user=cls.user,
            email=cls.user.email,
            verified=True,
            primary=True,
        )

    def test_11_login_view_get_method(self):
        """
        getメソッドにおいて、status_codeおよびtemplateの確認
        """
        response = self.client.get(login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_12_login_view_post_method(self):
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
        self.assertTemplateUsed(response, 'index.html')

class ProfileDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="test@test.com",
            password="test0000"
        )

        cls.profile = Profile.objects.get(user=cls.user)
        cls.profile.user=cls.user
        cls.profile.username="inital_username"
        cls.profile.name="inital_name"
        cls.profile.introduction="inital_text"
        cls.profile.bio=1
        cls.profile.birth=date(2000, 1, 1)
        cls.profile.workplace=1
        cls.profile.occapation=1
        cls.profile.industry=1
        cls.profile.position=1
        cls.profile.save()

    def test_24_access_profile_detail_view_logged_in(self):
        """
        ログイン状態でのstatus_codeおよびtemplateの確認
        """
        self.client.login(
            email='test@test.com',
            password='test0000'
        )

        response = self.client.get(profile_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/profile.html')
        self.assertContains(response, self.profile.username)

    def test_25_access_profile_detail_view_logged_out(self):
        """
        ログアウト状態でのstatus_codeおよびtemplateの確認
        """
        response = self.client.get(profile_detail_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/accounts/profile/')
        response = self.client.get('/accounts/login/?next=/accounts/profile/')
        self.assertTemplateUsed(response, 'account/login.html')

class ProfileUpdateViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="test@test.com",
            password="test0000"
        )

        cls.profile = Profile.objects.get(user=cls.user)
        cls.profile.user=cls.user
        cls.profile.username="inital_username"
        cls.profile.name="inital_name"
        cls.profile.introduction="inital_text"
        cls.profile.bio=1
        cls.profile.birth=date(2000, 1, 1)
        cls.profile.workplace=1
        cls.profile.occapation=1
        cls.profile.industry=1
        cls.profile.position=1
        cls.profile.save()

    def test_26_access_profile_update_view_logged_in(self):
        """
        ログイン状態でのstatus_codeおよびtemplateの確認
        """
        self.client.login(
            email='test@test.com',
            password='test0000'
        )

        response = self.client.get(profile_update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/profile.html')

    def test_27_profile_update_view_post_method(self):
        """
        postメソッドにより、データ内容が更新されているかを確認
        """
        self.client.login(
            email='test@test.com',
            password='test0000'
        )

        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_image:
            image = Image.new('RGB', (100, 100), color='red')
            image.save(temp_image, format='JPEG')
            temp_image.seek(0)
            update_image = SimpleUploadedFile(
                temp_image.name, temp_image.read(), content_type='image/jpeg'
            )

        updated_data = {
                'username': 'updated_username',
                'name': 'updated_name',
                'introduction': 'updated_text',
                'image': update_image,
                'bio': 2,
                'birth': date(2010, 1, 1),
                'workplace': 2,
                'occapation': 2,
                'industry': 2,
                'position': 2,
            }

        response = self.client.post(
            profile_update_url,
            updated_data,
            follow=True
            )

        self.assertRedirects(response, profile_detail_url)

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.username, 'updated_username')
        self.assertEqual(self.profile.name, 'updated_name')
        self.assertEqual(self.profile.introduction, 'updated_text')
        self.assertTrue(self.profile.image.name.endswith('.jpg'))
        self.assertEqual(self.profile.bio, 2)
        self.assertEqual(self.profile.birth, date(2010, 1, 1))
        self.assertEqual(self.profile.workplace, 2)
        self.assertEqual(self.profile.occapation, 2)
        self.assertEqual(self.profile.industry, 2)
        self.assertEqual(self.profile.position, 2)

        if self.profile.image:
            self.profile.image.delete()

    def test_28_profile_update_view_customized_form_valid_and_form_invalid(self):
        """
        カスタマイズしたform_validおよびform_invalidを確認
        """
        self.client.login(
            email='test@test.com',
            password='test0000'
        )

        profile = Profile.objects.get(user=self.user)

        # form_valid = True
        valid_data = {
            'username': 'correct_username',
            'name': self.profile.name,
            'introduction': self.profile.introduction,
            'bio': self.profile.bio,
            'birth': self.profile.birth,
            'workplace': self.profile.workplace,
            'occapation': self.profile.occapation,
            'industry': self.profile.industry,
            'position': self.profile.position,
            }

        response = self.client.post(profile_update_url, valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, profile_detail_url)

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.username, 'correct_username')

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, 'alert alert-success')
        self.assertEqual(messages[0].message, "プロフィールを更新しました")

        # form_valid = False
        # username
        invalid_data = {
            'username': 'InSpace username',
            'name': self.profile.name,
            'introduction': self.profile.introduction,
            'bio': self.profile.bio,
            'birth': self.profile.birth,
            'workplace': self.profile.workplace,
            'occapation': self.profile.occapation,
            'industry': self.profile.industry,
            'position': self.profile.position,
            }

        response = self.client.post(profile_update_url, invalid_data)
        self.assertEqual(response.status_code, 200)

        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertEqual(form.errors['username'], ['半角英字(小文字・大文字)、数字、アンダースコア(_)を組み合わせて作成してください。'])

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, 'alert alert-danger')
        self.assertEqual(messages[0].message, "プロフィールの更新に失敗しました")

        # birth
        future_day = date.today() + timedelta(days=365)

        invalid_data = {
            'username': self.profile.username,
            'name': self.profile.name,
            'introduction': self.profile.introduction,
            'bio': self.profile.bio,
            'birth': future_day,
            'workplace': self.profile.workplace,
            'occapation': self.profile.occapation,
            'industry': self.profile.industry,
            'position': self.profile.position,
            }

        response = self.client.post(profile_update_url, invalid_data)
        self.assertEqual(response.status_code, 200)

        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('birth', form.errors)
        self.assertEqual(form.errors['birth'], ['正しい生年月日を入力してください。'])

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, 'alert alert-danger')
        self.assertEqual(messages[0].message, "プロフィールの更新に失敗しました")
