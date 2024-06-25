from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

class UserModelTests(TestCase):
    def test_1_true_initial_state_is_empty(self):
        """
        初期状態において、登録データがないことを確認
        """
        user_obj = User.objects.all()
        self.assertEqual(user_obj.count(), 0)


    def test_2_true_user_object_creation(self):
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


    def test_3_true_email_raises_integrity_error(self):
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


    def test_4_true_create_user_without_email_raises_error(self):
        """
        新規登録時に'email'フィールドが未入力エラーの場合、エラーが発生するかを確認
        """
        with self.assertRaises(ValueError) as context:
            User.objects.create_user(
                email=None,
                password='test0000'
            )
        self.assertEqual(str(context.exception), 'メールアドレスを入力してください')


    def test_5_true_create_superuser(self):
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


    def test_6_true_meta_option_str_method(self):
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
