from django.test import TestCase
from django.contrib.auth import get_user_model
from app.models.post_models import Post
from django.core.exceptions import ValidationError

User = get_user_model()

class PostModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="main@test.com",
            password="test0000"
        )

    def test_42_initial_state_is_empty(self):
        """
        初期状態において、登録データがないことを確認
        """
        post_obj = Post.objects.all()
        self.assertEqual(post_obj.count(), 0)

    def test_43_post_object_creation(self):
        """
        1レコードを新規作成して保存動作を確認
        """
        post_data = Post(
            user = self.user,
            post_title = 'test_title',
            reason = 'test_reason',
            impressions = 'test_impressions',
            satisfaction = 3,

            book_title = 'test_book_title',
            author = 'test_author',
            isbn = 0000000000000
        )
        post_data.save()

        post_obj = Post.objects.all()
        self.assertEqual(post_obj.count(), 1)

        post_data = Post.objects.get(user=self.user)
        self.assertTrue(post_data.created_at)
        self.assertTrue(post_data.updated_at)

    def test_44_each_fields_validation(self):
        """
        各フィールドに設定したバリデーションを確認
        """
        post_obj = Post(
            user = self.user,
            post_title = 'test_title',
            reason = 'test_reason',
            impressions = 'test_impressions',
            satisfaction = 3,

            book_title = 'test_book_title',
            author = 'test_author',
            isbn = 0000000000000
        )
        post_obj.save()

        post_data = Post.objects.get(user=self.user)

        success_value_25 = 'x' * 25
        success_value_255 = 'x' * 255
        success_value_13 = 'x' * 13

        failure_value_over_25 = 'x' * 26
        failure_value_over_255 = 'x' * 256
        failure_value_over_13 = 'x' * 14

        # post_title
        post_data.post_title = failure_value_over_25
        with self.assertRaises(ValidationError):
            post_data.full_clean()

        post_data.post_title = success_value_25
        try:
            post_data.full_clean()
        except ValidationError:
            self.fail('"post_title: 正常値" のバリデーションに異常な挙動が発生')

        # reason
        post_data.reason = failure_value_over_25
        with self.assertRaises(ValidationError):
            post_data.full_clean()

        post_data.reason = success_value_25
        try:
            post_data.full_clean()
        except ValidationError:
            self.fail('"reason: 正常値" のバリデーションに異常な挙動が発生')

        # impressions
        post_data.impressions = failure_value_over_255
        with self.assertRaises(ValidationError):
            post_data.full_clean()

        post_data.impressions = success_value_255
        try:
            post_data.full_clean()
        except ValidationError:
            self.fail('"impressions: 正常値" のバリデーションに異常な挙動が発生')

        # satisfaction
        post_data.satisfaction = 0
        with self.assertRaises(ValidationError):
            post_data.full_clean()

        post_data.satisfaction = 6
        with self.assertRaises(ValidationError):
            post_data.full_clean()

        post_data.satisfaction = 3
        try:
            post_data.full_clean()
        except ValidationError:
            self.fail('"satisfaction: 正常値" のバリデーションに異常な挙動が発生')

        # book_title
        post_data.book_title = failure_value_over_255
        with self.assertRaises(ValidationError):
            post_data.full_clean()

        post_data.book_title = success_value_255
        try:
            post_data.full_clean()
        except ValidationError:
            self.fail('"book_title: 正常値" のバリデーションに異常な挙動が発生')

        # author
        post_data.author = failure_value_over_255
        with self.assertRaises(ValidationError):
            post_data.full_clean()

        post_data.author = success_value_255
        try:
            post_data.full_clean()
        except ValidationError:
            self.fail('"author: 正常値" のバリデーションに異常な挙動が発生')

        # isbn
        post_data.isbn = failure_value_over_13
        with self.assertRaises(ValidationError):
            post_data.full_clean()

        post_data.isbn = success_value_13
        try:
            post_data.full_clean()
        except ValidationError:
            self.fail('"isbn: 正常値" のバリデーションに異常な挙動が発生')

    def test_45_update_post_data(self):
        """
        データの更新を確認
        """
        post_obj = Post(
            user = self.user,
            post_title = 'test_title',
            reason = 'test_reason',
            impressions = 'test_impressions',
            satisfaction = 3,

            book_title = 'test_book_title',
            author = 'test_author',
            isbn = '0000000000000'
        )
        post_obj.save()

        update_post_title = 'update_title'
        update_reason = 'update_reason'
        update_impressions = 'update_impressions'
        update_satisfaction = 5
        update_book_title = 'update_book_title'
        update_author = 'update_author'
        update_isbn = '9999999999999'

        post_data = Post.objects.get(user=self.user)

        post_data.post_title = update_post_title
        post_data.reason = update_reason
        post_data.impressions = update_impressions
        post_data.satisfaction = update_satisfaction
        post_data.book_title = update_book_title
        post_data.author = update_author
        post_data.isbn = update_isbn

        post_data.save()
        post_data.refresh_from_db()

        post_data = Post.objects.get(user=self.user)
        self.assertEqual(post_data.post_title, update_post_title)
        self.assertEqual(post_data.reason, update_reason)
        self.assertEqual(post_data.impressions, update_impressions)
        self.assertEqual(post_data.satisfaction, update_satisfaction)
        self.assertEqual(post_data.book_title, update_book_title)
        self.assertEqual(post_data.author, update_author)
        self.assertEqual(post_data.isbn, update_isbn)
