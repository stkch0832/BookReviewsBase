from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models.profile_models import Profile
from config import settings
from allauth.account.models import EmailAddress
from datetime import date
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from django.contrib.messages import get_messages
from app.models.post_models import Post


User = get_user_model()
signup_url = reverse('accounts:accounts_signup')
login_url = reverse('accounts:accounts_login')
login_redirect_url = settings.LOGIN_REDIRECT_URL


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
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.com',
            password='password'
            )
        self.profile = Profile.objects.get(user=self.user)
        self.profile.username = 'test_user'
        self.profile.save()

        for i in range(13):
            Post.objects.create(
                user=self.user,
                post_title=f'no.{i}_Post',
                reason='reason',
                impressions='impressions',
                satisfaction=5,
                book_title='book_title',
                author='author',
                isbn='1234567890123'
            )

    def test_24_profile_detail_view_status_code_template_and_context(self):
        """
        存在するデータにアクセスした場合、status_code, template, contextの確認
        """
        response = self.client.get(
            reverse('accounts:profile_detail', kwargs={'username': self.profile.username})
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/profile_detail.html')

        self.assertIn('profile', response.context)
        self.assertIn('posts', response.context)
        self.assertIn('page_obj', response.context)

    def test_25_profile_detail_view_profile_not_exist(self):
        """
        存在しないデータにアクセスした場合、404エラーが発生するか確認
        """
        non_username='dummy_name'
        response = self.client.get(
            reverse('accounts:profile_detail', kwargs={'username': non_username})
            )
        self.assertEqual(response.status_code, 404)

    def test_74_profile_detail_view_pagination(self):
        """
        ページネーションの設定確認
        """
        response = self.client.get(
            reverse('accounts:profile_detail', kwargs={'username': self.profile.username})
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 5)

        response = self.client.get(
            reverse('accounts:profile_detail', kwargs={'username': self.profile.username}) + '?page=2'
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 5)

        response = self.client.get(
            reverse('accounts:profile_detail', kwargs={'username': self.profile.username}) + '?page=3'
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_75_profile_detail_view_pagination_invalid_page(self):
        """
        範囲外のページが指定された場合、最後のページに移動するか確認
        """
        response = self.client.get(
            reverse('accounts:profile_detail', kwargs={'username': self.profile.username}) + '?page=999'
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 3)
        self.assertEqual(response.context['page_obj'].number, 3)


class ProfileUpdateViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.com',
            password='test0000'
            )
        self.profile = Profile.objects.get(user_id=self.user.id)
        self.profile.username='test_user'
        self.profile.name='Test User'
        self.profile.introduction='Test introduction.'
        self.profile.bio=1
        self.profile.birth=date(2000, 1, 1,)
        self.profile.workplace=1
        self.profile.occapation=1
        self.profile.industry=1
        self.profile.position=1
        self.profile.image='test_image.jpg'
        self.profile.save()

    def test_26_request_get_method_if_not_logged_in_user(self):
        """
        getメソッドにて、ログインしていないユーザーがアクセスした場合の確認
        """
        self.client.logout()
        response = self.client.get(reverse('accounts:profile_edit'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/accounts/profile/edit/')

    def test_27_request_get_method_by_user_response_status_code_temolate_and_form_inital(self):
        """
        getメソッドにて、ユーザーが正常にアクセスした場合、status_code, template, form_initialの確認
        """
        self.client.login(
            email='test@test.com',
            password='test0000'
            )
        response = self.client.get(reverse('accounts:profile_edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/profile_form.html')

        form = response.context['form']
        self.assertEqual(form.initial['username'], 'test_user')
        self.assertEqual(form.initial['name'], 'Test User')

    def test_28_request_post_method_profile_update(self):
        """
        postメソッドにて、正常にデータ更新されているかを確認
        """
        self.client.login(
            email='test@test.com',
            password='test0000'
            )

        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_image:
            image = Image.new('RGB', (100, 100), color='red')
            image.save(temp_image, format='JPEG')
            temp_image.seek(0)
            new_image = SimpleUploadedFile(
                temp_image.name, temp_image.read(), content_type='image/jpeg'
            )

        response = self.client.post(
            reverse('accounts:profile_edit'), {
            'username': 'new_user',
            'name': 'New User',
            'introduction': 'New introduction.',
            'bio': 2,
            'birth': date(2010, 1, 1),
            'workplace': 2,
            'occapation': 2,
            'industry': 2,
            'position': 2,
            'image': new_image
        })
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.username, 'new_user')
        self.assertEqual(self.profile.name, 'New User')
        self.assertEqual(self.profile.introduction, 'New introduction.')
        self.assertRedirects(response, reverse('accounts:profile_edit'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, 'alert alert-success')
        self.assertEqual(messages[0].message, 'プロフィールを変更しました。')

class AccountDeleteViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.com',
            password='test0000'
            )
        self.profile = Profile.objects.get(user=self.user)
        self.post = Post.objects.create(
            user=self.user,
            post_title='Test Post',
            reason='Test Reason',
            impressions='Test Impressions',
            satisfaction=5,
            book_title='Test Book Title',
            author='Test Author',
            isbn='1234567890123'
            )

        self.client = Client()
        self.client.login(
            email='test@test.com',
            password='test0000'
            )

    def test_71_logged_in_user_delete_self_account_success(self):
        """
        ログインしたユーザーにて、アカウントを削除した場合、User, Profile, Postの各データが削除されたかを確認
        """
        response = self.client.post(reverse('accounts:accounts_delete'))
        self.assertRedirects(response, reverse('app:post_list'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'アカウントを削除しました。ご利用いただきありがとうございました。')

        with self.assertRaises(User.DoesNotExist):
            User.objects.get(email='test@test.com')

        with self.assertRaises(Profile.DoesNotExist):
            Profile.objects.get(user=self.user)

        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(user=self.user)

    def test_72_logged_in_user_delete_account_failed(self):
        """
        ログインをしていないユーザーにて、アクセスした場合
        """
        self.client.logout()
        response = self.client.post(reverse('accounts:accounts_delete'))
        self.assertRedirects(response, f"{reverse('account_login')}?next={reverse('accounts:accounts_delete')}")


    def tearDown(self):
        self.user.delete()
        self.profile.delete()
        self.post.delete()
