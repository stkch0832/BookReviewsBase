from django.test import TestCase
from django.contrib.auth import get_user_model
from app.models.post_models import Post
from django.core.exceptions import ValidationError
from app.models.comment_models import Comment

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

class CommentModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.post_user = User.objects.create_user(
            email="post_user@test.com",
            password="test0000"
        )
        cls.comment_user = User.objects.create_user(
            email="comment_user@test.com",
            password="test0000"
        )
        cls.post = Post.objects.create(
            user=cls.post_user,
            post_title="post_title",
            reason="reason",
            impressions="impressions",
            satisfaction=5,
            book_title="book_title",
            author="author",
            isbn="0000000000000",
        )

    def test_75_initial_state_is_empty(self):
        """
        初期状態において、登録データがないことを確認
        """
        comment_obj = Comment.objects.all()
        self.assertEqual(comment_obj.count(), 0)

    def test_76_comment_object_creation(self):
        """
        1レコードを新規作成して保存動作を確認
        """
        comment_data = Comment(
            user = self.comment_user,
            comment = "test comment",
            post = self.post,
        )
        comment_data.save()

        comment_data.refresh_from_db()
        comment_obj = Comment.objects.all()
        self.assertEqual(comment_obj.count(), 1)

        comment_data = Comment.objects.get(id=1)
        self.assertEqual(comment_data.user_id, self.comment_user.pk)
        self.assertEqual(comment_data.comment, "test comment")
        self.assertEqual(comment_data.post_id, self.post.pk)
        self.assertTrue(comment_data.created_at)

    def test_77_comment_field_validation(self):
        """
        commentフィールドのmax_lengthのバリデーションを確認
        """

        failure_comment = "x" * 256
        success_comment = "x" * 255

        comment_data = Comment(
            user = self.comment_user,
            comment = failure_comment,
            post = self.post,
        )

        with self.assertRaises(ValidationError):
            comment_data.full_clean()

        comment_data.comment = success_comment
        try:
            comment_data.full_clean()
        except ValidationError:
            self.fail('"comment: 正常値" のバリデーションに異常な挙動が発生')
