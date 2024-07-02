from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from accounts.models.profile_models import Profile
import string, random
from django.core.exceptions import ValidationError
from datetime import date, timedelta
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

User = get_user_model()

class UserModelTests(TestCase):
    def test_1_initial_state_is_empty(self):
        """
        初期状態において、登録データがないことを確認
        """
        user_obj = User.objects.all()
        self.assertEqual(user_obj.count(), 0)


    def test_2_user_object_creation(self):
        """
        1レコードを新規作成し、保存動作を確認
        """
        user_obj = User(
            email='test@test.com',
            password='test1234'
        )
        user_obj.save()

        user_data = User.objects.all()
        self.assertEqual(user_data.count(), 1)


    def test_3_email_raises_integrity_error(self):
        """
        登録できるメールアドレスはDB内で一意制約があることを確認
        """
        test_email = 'test@test.com'

        user_first = User(
            email=test_email,
            password='test1111'
        )
        user_first.save()

        user_secound = User(
            email=test_email,
            password='test2222'
        )

        with self.assertRaisesMessage(IntegrityError, "UNIQUE constraint failed: users.email"):
            User.objects.create_user(
                email=user_secound.email,
                password=user_secound.password
            )


    def test_4_create_user_without_email_raises_error(self):
        """
        新規登録時に'email'フィールドが未入力エラーの場合、エラーが発生するかを確認
        """
        with self.assertRaises(ValueError) as context:
            User.objects.create_user(
                email=None,
                password='test0000'
            )
        self.assertEqual(str(context.exception), 'メールアドレスを入力してください')


    def test_5_create_superuser(self):
        """
        スーパーユーザー作成時のデフォルト値の確認
        """
        admin_user = User.objects.create_superuser(
            email = 'admin@test.com',
            password = 'admin0000'
        )

        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertEqual(admin_user.email, 'admin@test.com')
        self.assertTrue(admin_user.check_password('admin0000'))


    def test_6_meta_option_str_method(self):
        """
        Metaオプションのstrメソッドにおいて、返り値が'email'フィールドの値であることを確認
        """
        user_obj = User(
            email='test@test.com',
            password='test1234'
        )
        user_obj.save()

        user_data = User.objects.get(email='test@test.com')
        self.assertEqual(str(user_data), user_data.email)

class ProfileModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="main@test.com",
            password="test0000"
        )

    def test_13_auto_create_profile_related_user_data_when_create_user(self):
        """
        Userデータの新規作成により、user_idで紐付けされたProfileデータが自動作成されていることを確認
        """
        profile_obj = Profile.objects.all()
        self.assertEqual(profile_obj.count(), 1)

        profile_data = Profile.objects.get(user=self.user)
        profile_user_id = profile_data.user_id

        self.assertEqual(profile_user_id, self.user.id)

    def test_14_each_profile_model_fields_defalut_value(self):
        """
        modelフィールドで個別に設定したデフォルト値を確認
        """
        profile_data = Profile.objects.get(user=self.user)

        self.assertEqual(len(profile_data.username), 16)
        self.assertEqual(profile_data.name, '名無し')
        self.assertFalse(profile_data.image)
        self.assertEqual(profile_data.workplace, 0)
        self.assertEqual(profile_data.occapation, 0)
        self.assertEqual(profile_data.industry, 0)
        self.assertEqual(profile_data.position, 0)

    def test_15_username_validation(self):
        """
        usernameフィールドに設定したバリデーションを確認
        """
        chars = string.ascii_letters + string.digits + '_'
        length = 0

        def create_username(chars, length):
            test_username = ''.join(random.choices(chars, k=length))
            return test_username

        main_user = User.objects.get(email='main@test.com')
        main_user_profile = Profile.objects.get(user=main_user)

        # max_length: true
        length = 30
        username_true = create_username(chars, length)
        main_user_profile.username = username_true
        try:
            main_user_profile.full_clean()
        except ValidationError:
            self.fail('"username-max_length: 正常値" のバリデーションに異常な挙動が発生')

        # max_length: false
        length = 31
        username_false = create_username(chars, length)
        main_user_profile.username = username_false
        with self.assertRaises(ValidationError):
            main_user_profile.full_clean()

        # min_length: false
        length = 4
        username_false = create_username(chars, length)
        main_user_profile.username = username_false
        with self.assertRaises(ValidationError):
            main_user_profile.full_clean()

        # unique
        username_sample = 'unique_name'

        User.objects.create_user(
            email="sub@test.com",
            password="test0000"
        )

        another_user = User.objects.get(email='sub@test.com')
        another_user_profile = Profile.objects.get(user=another_user)
        another_user_profile.username = username_sample
        another_user_profile.save()

        main_user_profile.username = username_sample
        with self.assertRaises(ValidationError):
            main_user_profile.full_clean()

        # regex
        invalid_usernames = [
            'inSpace username',
            'inDash-username',
            'inSpecialCharacters@username',
            'in全角_username'
            ]
        for invalid_username in invalid_usernames:
            main_user_profile.username = invalid_username
            with self.assertRaises(ValidationError):
                main_user_profile.full_clean()

    def test_16_name_validation(self):
        """
        nameフィールドに設定したバリデーションを確認
        """
        length = 0

        def create_name_unicode_string(length):
            return ''.join(chr(random.randint(0x4E00, 0x9FFF)) for _ in range(length))

        user = User.objects.get(email='main@test.com')
        profile = Profile.objects.get(user=user)

        # max_length: true
        length = 30
        name_true = create_name_unicode_string(length)
        profile.name = name_true
        try:
            profile.full_clean()
        except ValidationError:
            self.fail('"name-max_length: 正常値" のバリデーションに不備が発生')

        # max_length: false
        length = 31
        name_false = create_name_unicode_string(length)
        profile.name = name_false
        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_17_introduction_validation(self):
        """
        introductionフィールドに設定したバリデーションを確認
        """
        length = 0

        def create_introduction_unicode_string(length):
            return ''.join(chr(random.randint(0x4E00, 0x9FFF)) for _ in range(length))

        user = User.objects.get(email='main@test.com')
        profile = Profile.objects.get(user=user)

        # max_length: true
        length = 255
        introduction_true = create_introduction_unicode_string(length)
        profile.introduction = introduction_true
        try:
            profile.full_clean()
        except ValidationError:
            self.fail('"introduction-max_length: 正常値" のバリデーションに不備が発生')

        # max_length: false
        length = 256
        introduction_false = create_introduction_unicode_string(length)
        profile.introduction = introduction_false
        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_18_calclate_age_include_customized_save_method(self):
        """
        saveメソッドをカスタマイズした年齢の自動算出を確認
        """
        profile = Profile.objects.get(user=self.user)
        self.assertFalse(profile.age)

        today = date.today()
        twenty_years_ago = today - timedelta(days=365 * 20 + 5)
        profile.birth = twenty_years_ago
        profile.save()
        self.assertTrue(profile.birth)
        self.assertEqual(profile.age, 20)

    def test_19_update_profile_data(self):
        """
        profileデータの更新後の保存データを確認
        """
        profile = Profile.objects.get(user=self.user)
        age = 40

        update_username = 'Unique_username'
        update_name = 'テストユーザー'
        update_introduction = 'Text'
        update_bio = 1
        update_birth = date.today() - timedelta(days=365 * age + 10)
        update_workplace = 2
        update_occapation = 3
        update_industry = 4
        update_position = 5

        # ダミーデータを作成・格納
        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_image:
            image = Image.new('RGB', (100, 100), color = 'red')
            image.save(temp_image, format='JPEG')
            temp_image.seek(0)
            update_image = SimpleUploadedFile(temp_image.name, temp_image.read())

        profile.username = update_username
        profile.name = update_name
        profile.introduction = update_introduction
        profile.image = update_image
        profile.bio = update_bio
        profile.birth = update_birth
        profile.workplace = update_workplace
        profile.occapation = update_occapation
        profile.industry = update_industry
        profile.position = update_position

        profile.save()

        profile.refresh_from_db()
        profile = Profile.objects.get(user=self.user)

        self.assertEqual(profile.username, update_username)
        self.assertEqual(profile.name, update_name)
        self.assertEqual(profile.introduction, update_introduction)
        self.assertTrue(profile.image)
        self.assertTrue(profile.image.name.endswith('.jpg'))
        self.assertEqual(profile.bio, update_bio)
        self.assertEqual(profile.birth, update_birth)
        self.assertEqual(profile.age, age)
        self.assertEqual(profile.workplace, update_workplace)
        self.assertEqual(profile.occapation, update_occapation)
        self.assertEqual(profile.industry, update_industry)
        self.assertEqual(profile.position, update_position)

        if profile.image:
                profile.image.delete()
