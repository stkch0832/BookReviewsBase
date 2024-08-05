from django.test import TestCase
from app.forms.book_forms import BookSearchForm
from app.forms.post_forms import PostForm, SATISFACTION_CHOICES
from django.contrib.auth import get_user_model
from app.forms.comment_forms import CommentForm
from app.models.post_models import Post


User = get_user_model()

class BookSearchFormTests(TestCase):

    def test_31_form_initialization(self):
        """
        フォームの初期化した際の各属性の設定を確認
        """
        form = BookSearchForm()
        self.assertEqual(form.fields['title'].label, '本のタイトル')
        self.assertTrue(form.fields['title'].required)

        self.assertEqual(form.fields['author'].label, '著者名')

    def test_32_form_validation_valid_data(self):
        """
        フォームの有効性を確認
        """
        form_data = {
            'title': 'test_title',
            'author': 'test_author',
        }
        form = BookSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_33_custmized_form_validation_in_title_field(self):
        """
        カスタマイズしたtitleフィールドのバリデーションを確認
        """
        # required
        form_data = {
            'title': '',
            'author': 'test_author',
        }
        form = BookSearchForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        # print(form.errors['title'])

class PostFormTests(TestCase):

    def test_46_form_initialization(self):
        """
        フォームの初期化した際の各属性の設定を確認
        """
        book_data = {
            'title': 'test_title',
            'author': 'test_author',
            'isbn': '0000000000000'
        }

        form = PostForm(book_data=book_data)

        self.assertEqual(form.fields['impressions'].label, '所感')

        self.assertEqual(form.fields['satisfaction'].label, '満足度')
        self.assertEqual(form.fields['satisfaction'].choices, SATISFACTION_CHOICES)

        self.assertEqual(form.fields['book_title_display'].label, '本のタイトル')
        self.assertEqual(form.fields['book_title_display'].required, False)
        self.assertEqual(form.fields['book_title_display'].disabled, True)

        self.assertEqual(form.fields['author_display'].label, '著者名')
        self.assertEqual(form.fields['author_display'].required, False)
        self.assertEqual(form.fields['author_display'].disabled, True)

        self.assertEqual(form.fields['isbn_display'].label, 'ISBNコード')
        self.assertEqual(form.fields['isbn_display'].required, False)
        self.assertEqual(form.fields['isbn_display'].disabled, True)

        self.assertEqual(form.fields['book_title_display'].initial, book_data['title'])
        self.assertEqual(form.fields['author_display'].initial, book_data['author'])
        self.assertEqual(form.fields['isbn_display'].initial, book_data['isbn'])

        self.assertEqual(
            form.fields['post_title'].widget.attrs['placeholder'],
            '25文字以内'
            )
        self.assertEqual(
            form.fields['reason'].widget.attrs['placeholder'],
            '25文字以内'
            )
        self.assertEqual(
            form.fields['impressions'].widget.attrs['placeholder'],
            '25文字以内'
            )

    def test_47_each_form_field_raise_error_because_none_value(self):
        """
        各フィールドにおいて、未入力でpostした場合に未入力エラーになるか確認
        """
        form_data = {
            'post_title': '',
            'reason': '',
            'impressions': '',
            'satisfaction': '',
        }

        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())

        self.assertIn('post_title', form.errors)
        self.assertIn('reason', form.errors)
        self.assertIn('impressions', form.errors)
        self.assertIn('satisfaction', form.errors)

class CommentFormTests(TestCase):
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

    def test_78_form_validation_valid_data(self):
        """
        フォームの有効性を確認
        """
        form_data = {
            'user': self.comment_user,
            'comment': 'test_author',
            'post': self.post_user,
        }
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_79_comment_field_raise_error_because_none_value(self):
        """
        commentフィールドにおいて、未入力でpostした場合に未入力エラーになるか確認
        """
        form_data = {
            'user': self.comment_user,
            'comment': '',
            'post': self.post_user,
        }

        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())

        self.assertIn('comment', form.errors)
