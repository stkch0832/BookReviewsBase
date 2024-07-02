from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models.profile_models import Profile
from accounts.forms.user_forms import CustomSignupForm
from accounts.forms.profile_forms import ProfileForm
from datetime import date, timedelta
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from django import forms


User = get_user_model()

class CustomSignupFormTests(TestCase):

    def test_7_signup_new_account(self):
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


    def test_8_clean_email_method(self):
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

class ProfileFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.main_user = User.objects.create_user(
            email="main@test.com",
            password="test0000"
        )

        cls.main_profile = Profile.objects.get(user=cls.main_user)
        cls.main_profile.user=cls.main_user
        cls.main_profile.username="inital_username"
        cls.main_profile.name="inital_name"
        cls.main_profile.introduction="inital_text"
        cls.main_profile.bio=1
        cls.main_profile.birth=date(2000, 1, 1)
        cls.main_profile.workplace=1
        cls.main_profile.occapation=1
        cls.main_profile.industry=1
        cls.main_profile.position=1

        cls.sub_user = User.objects.create_user(
            email="sub@test.com",
            password="test0000"
        )

        cls.sub_profile = Profile.objects.get(user=cls.sub_user)
        cls.sub_profile.user=cls.sub_user
        cls.sub_profile.username="sub_username"
        cls.sub_profile.save()

    def test_20_submit_profile_form(self):
        """
        フォームからのデータ更新の有効性確認
        """
        form = ProfileForm(instance=self.main_profile)

        self.assertEqual(form.initial['username'], 'inital_username')
        self.assertEqual(form.initial['name'], 'inital_name')
        self.assertEqual(form.initial['introduction'], 'inital_text')
        self.assertEqual(form.initial['bio'], 1)
        self.assertEqual(form.initial['birth'], date(2000, 1, 1))
        self.assertEqual(form.initial['workplace'], 1)
        self.assertEqual(form.initial['occapation'], 1)
        self.assertEqual(form.initial['industry'], 1)
        self.assertEqual(form.initial['position'], 1)

        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_image:
            image = Image.new('RGB', (100, 100), color = 'red')
            image.save(temp_image, format='JPEG')
            temp_image.seek(0)
            update_image = SimpleUploadedFile(
                temp_image.name, temp_image.read(), content_type='image/jpeg'
            )
        update_data = {
            'username': 'update_username',
            'name': 'update_name',
            'introduction': 'update_text',
            'image': update_image,
            'bio': 2,
            'birth': date(2010, 12, 31),
            'workplace': 2,
            'occapation': 2,
            'industry': 2,
            'position': 2,
        }

        form = ProfileForm(
            instance=self.main_profile,
            data=update_data,
            files={'image': update_image}
            )

        self.assertTrue(form.is_valid())
        form.save()

        self.main_profile.refresh_from_db()

        self.assertEqual(self.main_profile.username, 'update_username')
        self.assertEqual(self.main_profile.name, 'update_name')
        self.assertEqual(self.main_profile.introduction, 'update_text')
        self.assertTrue(self.main_profile.image.name.endswith('.jpg'))
        self.assertEqual(self.main_profile.bio, 2)
        self.assertEqual(self.main_profile.birth, date(2010, 12, 31))
        self.assertEqual(self.main_profile.workplace, 2)
        self.assertEqual(self.main_profile.occapation, 2)
        self.assertEqual(self.main_profile.industry, 2)
        self.assertEqual(self.main_profile.position, 2)

        if self.main_profile.image:
            self.main_profile.image.delete()

    def test_21_custmized_form_validation_in_username_field(self):
        """
        カスタマイズしたusernameフィールドのバリデーションを確認
        """
        form = ProfileForm(instance=self.main_profile)

        # max_length
        update_data = {
            'username': 'x' * 31,
        }

        form = ProfileForm(
            instance=self.main_profile,
            data=update_data
            )
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        # print(form.errors['username'])

        # min_length
        update_data = {
            'username': 'x' * 1,
        }

        form = ProfileForm(
            instance=self.main_profile,
            data=update_data
            )
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        # print(form.errors['username'])

        # regex
        invalid_usernames = [
            'inSpace username',
            'inDash-username',
            'inSpecialCharacters@username',
            'in全角_username'
        ]

        for invalid_username in invalid_usernames:
            update_data = {
                'username': invalid_username,
            }
        form = ProfileForm(
            instance=self.main_profile,
            data=update_data
        )
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertEqual(form.errors['username'], ['半角英字(小文字・大文字)、数字、アンダースコア(_)を組み合わせて作成してください。'])

        # required
        update_data = {
            'username': '',
        }

        form = ProfileForm(
            instance=self.main_profile,
            data=update_data
            )
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        # print(form.errors['username'])

    def test_22_clean_username_method(self):
        """
        clean_usernameのバリデーションを確認
        """
        valid_usernames = [
            'username1',
            'Username2',
            'user_name3'
        ]
        for valid_username in valid_usernames:
            form = ProfileForm(
                instance=self.main_profile,
                data={
                'username': valid_username,
                'name': self.main_profile.name,
                'introduction': self.main_profile.introduction,
                'bio': self.main_profile.bio,
                'birth': self.main_profile.birth,
                'workplace': self.main_profile.workplace,
                'occapation': self.main_profile.occapation,
                'industry': self.main_profile.industry,
                'position': self.main_profile.position,
            })
            form.cleaned_data = {'username': valid_username}
            try:
                form.clean_username()
            except forms.ValidationError:
                self.fail(f'clean_username() の挙動に異常が発生( {valid_username})')
        invalid_username_exist = {
            'username': self.sub_profile.username,
            'name': self.main_profile.name,
            'introduction': self.main_profile.introduction,
            'bio': self.main_profile.bio,
            'birth': self.main_profile.birth,
            'workplace': self.main_profile.workplace,
            'occapation': self.main_profile.occapation,
            'industry': self.main_profile.industry,
            'position': self.main_profile.position,
        }
        form = ProfileForm(data=invalid_username_exist)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertEqual(form.errors['username'], ['このユーザーIDは、既に使用されています。'])

        invalid_usernames_regex = [
            'inSpace username',
            'inDash-username',
            'inSpecialCharacters@username',
            'in全角_username'
        ]
        for invalid_username in invalid_usernames_regex:
            form = ProfileForm(instance=self.main_profile, data={
                'username': invalid_username,
                'name': self.main_profile.name,
                'introduction': self.main_profile.introduction,
                'bio': self.main_profile.bio,
                'birth': self.main_profile.birth,
                'workplace': self.main_profile.workplace,
                'occapation': self.main_profile.occapation,
                'industry': self.main_profile.industry,
                'position': self.main_profile.position,
            })

            form.cleaned_data = {'username': invalid_username}

            self.assertFalse(form.is_valid())
            self.assertIn('username', form.errors)
            self.assertEqual(form.errors['username'], ['半角英字(小文字・大文字)、数字、アンダースコア(_)を組み合わせて作成してください。'])

    def test_23_clean_birth_method(self):
        """
        clean_birthのバリデーションを確認
        """
        form = ProfileForm(instance=self.main_profile)

        future_day = date.today() + timedelta(days=365)

        update_data = {
            'birth': future_day,
        }
        form = ProfileForm(
            instance=self.main_profile,
            data=update_data
            )
        self.assertFalse(form.is_valid())
        self.assertIn('birth', form.errors)
        self.assertEqual(form.errors['birth'], ['正しい生年月日を入力してください。'])

    def test_29_custmized_form_validation_in_introduction_field(self):
        """
        カスタマイズしたintroductionフィールドのバリデーションを確認
        """
        form = ProfileForm(instance=self.main_profile)

        update_data = {
            'introduction': 'x' * 256,
        }

        form = ProfileForm(
            instance=self.main_profile,
            data=update_data
            )
        self.assertFalse(form.is_valid())
        self.assertIn('introduction', form.errors)

    def test_30_custmized_form_validation_in_name_field(self):
        """
        カスタマイズしたnameフィールドのバリデーションを確認
        """
        form = ProfileForm(instance=self.main_profile)

        # max_length
        update_data = {
            'name': 'x' * 31,
        }

        form = ProfileForm(
            instance=self.main_profile,
            data=update_data
            )
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

        # required
        update_data = {
            'name': '',
        }

        form = ProfileForm(
            instance=self.main_profile,
            data=update_data
            )
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        # print(form.errors['name'])
