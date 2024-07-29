import unittest
from unittest.mock import patch
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from app.models.post_models import Post
from django.utils import timezone
from django.contrib.messages import get_messages

User = get_user_model()

class BookSearchViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.book_search_url = reverse('app:book_search')

    def test_37_get_method(self):
        """
        getメソッドにおいて、status_codeおよびtemplateの確認
        """
        response = self.client.get(self.book_search_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/book_form.html')

    @patch('app.views.book_views.get_api_data')
    def test_38_post_method_response_success_with_results(self, mock_get_api_data):
        """
        postメソッドにおいて、有効なフォームデータにより、APIが成功、かつ、結果がある場合
        """
        mock_get_api_data.return_value = [{
            'Item': {
                'title': 'test_title',
                'author': 'test_author',
                'isbn': '1234567890',
                'largeImageUrl':'http://example.com/image.jpg'
                }
            }]

        # input only 'title'
        response = self.client.post(
            self.book_search_url,
            data={'title': 'test'}
            )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/book_list.html')
        self.assertContains(response, 'test_title', html=True)
        self.assertIn('http://example.com/image.jpg', response.content.decode('utf-8'))

        # input 'title' and 'author'
        response = self.client.post(
            self.book_search_url,
            data={
                'title': 'test_title',
                'author': 'test_author',
                }
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/book_list.html')
        self.assertContains(response, 'test_title test_authorの検索結果', html=True)
        self.assertIn('http://example.com/image.jpg', response.content.decode('utf-8'))


    @patch('app.views.book_views.get_api_data')
    def test_39_post_method_response_success_no_results(self, mock_get_api_data):
        """
        postメソッドにおいて、有効なフォームデータにより、APIが成功、かつ、結果がない場合
        """
        mock_get_api_data.return_value = None

        response = self.client.post(
            self.book_search_url,
            data={'title': 'test'}
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/book_list.html')
        self.assertContains(response, '該当するものがありません', html=True)

    @patch('app.views.book_views.get_api_data')
    def test_40_post_method_response_failure(self, mock_get_api_data):
        """
        postメソッドにおいて、有効なフォームデータであるが、APIが失敗した場合
        """
        mock_get_api_data.side_effect = Exception("API call failed")
        response = self.client.post(
            self.book_search_url,
            data={'title': 'test'}
            )
        self.assertEqual(response.status_code, 500)

    @patch('app.views.book_views.get_api_data')
    def test_41_post_method_response_form_invalid(self, mock_get_api_data):
        """
        postメソッドにおいて、無効なフォームデータであった場合
        """
        response = self.client.post(
            self.book_search_url,
            data={}
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/book_form.html')

if __name__ == '__main__':
    unittest.main()

class PostListViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='test@test.com',
            password='test0000'
            )

        number_of_posts = 13
        for post_num in range(number_of_posts):
            Post.objects.create(
                user=cls.user,
                post_title=f'Test Post {post_num}',
                reason=f'Test Reason {post_num}',
                impressions=f'Test Impressions {post_num}',
                satisfaction=5,
                book_title=f'Test Book Title {post_num}',
                author=f'Test Author {post_num}',
                isbn='1234567890123',
                created_at=timezone.now(),
                updated_at=timezone.now()
            )

    def test_48_check_url_statusCode_and_template_when_access_view(self):
        """
        PostListViewにアクセスし、URL, status_code, templateを確認
        """
        response = self.client.get('/bookreviewsbase/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('app:post_list'))
        self.assertTemplateUsed(response, 'index.html')
        self.assertEqual(response.status_code, 200)

    def test_49_how_many_displayed_items_in_a_page(self):
        """
        ページネーションの設定確認（paginate_by）
        """
        response = self.client.get(reverse('app:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertEqual(len(response.context['posts']), 5)

    def test_50_how_many_displayed_items_each_page(self):
        """
        ページネーションにより、各ページに表示される件数を確認
        FYI: number_of_posts = 13
        """
        # 最初のページ
        response = self.client.get(reverse('app:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['posts']), 5)

        # 2ページ目
        response = self.client.get(reverse('app:post_list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['posts']), 5)

        # 3ページ目（最後のページ）
        response = self.client.get(reverse('app:post_list') + '?page=3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['posts']), 3)

    def test_51_customized_context_object_name(self):
        """
        カスタマイズしたcontext_object_nameの確認
        """
        response = self.client.get(reverse('app:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('posts', response.context)
        self.assertEqual(len(response.context['posts']), 5)

class PostDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='test@test.com',
            password='testpassword'
            )

        cls.post = Post.objects.create(
            user=cls.user,
            post_title='Test Post',
            reason='Test Reason',
            impressions='Test Impressions',
            satisfaction=5,
            book_title='Test Book Title',
            author='Test Author',
            isbn='1234567890123',
            created_at=timezone.now(),
            updated_at=timezone.now()
        )


    def test_52_check_url_statusCode_and_template_when_access_view(self):
        """
        PostDetailViewにアクセスし、URL, status_code, templateを確認
        """
        response = self.client.get(f'/bookreviewsbase/posts/{self.post.pk}/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('app:post_detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/post_detail.html')


    @patch('app.views.post_views.get_api_data')
    def test_53_call_get_api_data_method_success(self, mock_get_api_data):
        """
        API接続・データ取得が成功した場合の確認
        """
        mock_get_api_data.return_value = [{
            'Item': {
                'title': 'Sample Title',
                'largeImageUrl': 'http://example.com/image.jpg',
                'author': 'Sample Author',
                'salesDate': '2020-01-01',
                'publisherName': 'Sample Publisher',
                'isbn': '1234567890123',
                'itemCaption': 'Sample Caption',
                'itemUrl': 'http://example.com',
                'reviewAverage': '4.5',
                'reviewCount': '10'
            }
        }]

        response = self.client.get(reverse('app:post_detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('book_data', response.context)
        self.assertEqual(response.context['book_data']['title'], 'Sample Title')

    @patch('app.views.post_views.get_api_data')
    def test_54_call_get_api_data_method_faile(self, mock_get_api_data):
        """
        API接続・データ取得が失敗した場合の確認
        """
        mock_get_api_data.return_value = None

        response = self.client.get(reverse('app:post_detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('error_message', response.context)
        self.assertEqual(response.context['error_message'], 'APIのリクエストに失敗しました。')

    @patch('app.views.post_views.get_api_data')
    def test_55_call_get_api_data_method_success_however_get_items_is_nothing(self, mock_get_api_data):
        """
        API接続は成功、取得したデータがなかった場合
        """
        mock_get_api_data.return_value = []

        response = self.client.get(reverse('app:post_detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('error_message', response.context)
        self.assertEqual(response.context['error_message'], '該当のデータがありません。')

    def test_56_customized_context_data(self):
        """
        カスタマイズしたcontext_dataの確認
        """
        response = self.client.get(reverse('app:post_detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('post_data', response.context)
        self.assertEqual(response.context['post_data'], self.post)

class PostCreateViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='test@test.com',
            password='test0000'
            )

    def setUp(self):
        self.client = Client()
        self.client.login(
            email='test@test.com',
            password='test0000'
            )
        self.isbn = '1234567890123'

    @patch('app.views.post_views.get_api_data')
    def test_57_get_request_api_success(self, mock_get_api_data):
        """
        getメッソドにて、API接続が成功、かつ、データを取得した場合のtemplate, status_code, context を確認
        """
        mock_get_api_data.return_value = [{
            'Item': {
                'title': 'Sample Title',
                'author': 'Sample Author',
                'isbn': '1234567890123',
                'largeImageUrl': 'http://example.com/image.jpg'
            }
        }]

        response = self.client.get(reverse('app:post_new', args=[self.isbn]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/post_form.html')
        self.assertIn('form', response.context)
        self.assertIn('book_data', response.context)
        self.assertEqual(response.context['book_data']['title'], 'Sample Title')

    @patch('app.views.post_views.get_api_data')
    def test_58_get_request_api_failure(self, mock_get_api_data):
        """
        getメッソドにて、API接続に失敗した場合のtemplate, status_code, context を確認
        """
        mock_get_api_data.return_value = None

        response = self.client.get(reverse('app:post_new', args=[self.isbn]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/book_form.html')
        self.assertIn('error_message', response.context)
        self.assertEqual(response.context['error_message'], 'APIのリクエストに失敗しました。')

    @patch('app.views.post_views.get_api_data')
    def test_59_get_request_api_success_however_not_found_items(self, mock_get_api_data):
        """
        getメッソドにて、API接続に成功したが、該当のデータがなかった場合のtemplate, status_code, context を確認
        """
        mock_get_api_data.return_value = []

        response = self.client.get(reverse('app:post_new', args=[self.isbn]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/book_form.html')
        self.assertIn('error_message', response.context)
        self.assertEqual(response.context['error_message'], '該当のデータがありません。')

    @patch('app.views.post_views.get_api_data')
    def test_60_post_request_success(self, mock_get_api_data):
        """
        postメソッドにて、有効なデータでリクエストされた場合
        """
        mock_get_api_data.return_value = [{
            'Item': {
                'title': 'Sample Title',
                'author': 'Sample Author',
                'isbn': '1234567890123',
                'largeImageUrl': 'http://example.com/image.jpg'
            }
        }]

        post_data = {
            'post_title': 'Test Post',
            'reason': 'Test Reason',
            'impressions': 'Test Impressions',
            'satisfaction': 5,
            'book_title': 'Sample Title',
            'author': 'Sample Author',
            'isbn': '1234567890123',
        }

        response = self.client.post(reverse('app:post_new', args=[self.isbn]), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('app:post_list'))
        self.assertTrue(Post.objects.filter(post_title='Test Post').exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), '新規投稿をしました。')

    @patch('app.views.post_views.get_api_data')
    def test_61_post_request_invalid_form(self, mock_get_api_data):
        """
        postメソッドにて、無効なデータにおいてリクエストされた場合
        """
        mock_get_api_data.return_value = [{
            'Item': {
                'title': 'Sample Title',
                'author': 'Sample Author',
                'isbn': '1234567890123',
                'largeImageUrl': 'http://example.com/image.jpg'
            }
        }]

        post_data = {
            'post_title': '',
            'reason': '',
            'impressions': '',
            'satisfaction': '',
            'book_title': 'Sample Title',
            'author': 'Sample Author',
            'isbn': '1234567890123',
        }

        response = self.client.post(reverse('app:post_new', args=[self.isbn]), data=post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/post_form.html')
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)

class PostUpdateViewTests(TestCase):

    def setUp(self):
        self.main_user = User.objects.create_user(
            email='main@test.com',
            password='testpassword1'
            )
        self.other_user = User.objects.create_user(
            email='other@test.com',
            password='testpassword2'
            )
        self.post = Post.objects.create(
            user=self.main_user,
            post_title='Default Title',
            reason='Default Reason',
            impressions='Default Impressions',
            satisfaction=3,
            book_title='Default Book Title',
            author='Default Author',
            isbn='1234567890123'
        )

    def test_62_get_request_logged_in_and_owner(self):
        """
        getメッソドにて、ログイン済み、かつ、投稿ユーザーおいて、アクセスを確認
        """
        self.client.login(
            email='main@test.com',
            password='testpassword1'
            )

        response = self.client.get(reverse('app:post_edit', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/post_form.html')
        self.assertIn('form', response.context)
        self.assertEqual(response.context['form'].initial['post_title'], 'Default Title')

    def test_63_get_request_logged_in_and_other_user(self):
        """
        getメッソドにて、ログイン済み、かつ、他のユーザーにおいて、アクセスを確認
        """
        self.client.login(
            email='other@test.com',
            password='testpassword2'
            )

        response = self.client.get(reverse('app:post_edit', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'この投稿を編集する権限がありません。')

    def test_64_get_request_not_logged_in_user(self):
        """
        getメソッドにて、ログインしていないユーザーにおいて、アクセスを確認
        """
        self.client.logout()

        response = self.client.get(reverse('app:post_edit', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'この投稿を編集する権限がありません。')

    def test_65_post_request_success(self):
        """
        postメソッドにて、有効なフォームデータでリクエストされた場合
        """
        self.client.login(
            email='main@test.com',
            password='testpassword1'
            )

        post_data = {
            'post_title': 'Updated Title',
            'reason': 'Updated Reason',
            'impressions': 'Updated Impressions',
            'satisfaction': 5,
        }
        response = self.client.post(reverse('app:post_edit', args=[self.post.pk]), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('app:post_detail', kwargs={'pk': self.post.pk}))

        self.post.refresh_from_db()
        self.assertEqual(self.post.post_title, 'Updated Title')

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), '投稿内容を変更しました。')

    def test_66_post_request_invalid_form(self):
        """
        postメソッドにて、無効なフォームデータでリクエストされた場合
        """
        self.client.login(
            email='main@test.com',
            password='testpassword1'
            )
        post_data = {
            'post_title': '',
            'reason': '',
            'impressions': '',
            'satisfaction': '',
        }
        response = self.client.post(reverse('app:post_edit', args=[self.post.pk]), data=post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/post_form.html')
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)

class PostDeleteViewTests(TestCase):

    def setUp(self):
        self.main_user = User.objects.create_user(
            email='main@test.com',
            password='testpassword1'
            )
        self.other_user = User.objects.create_user(
            email='other@test.com',
            password='testpassword2'
            )
        self.post = Post.objects.create(
            user=self.main_user,
            post_title='Test Title',
            reason='Test Reason',
            impressions='Test Impressions',
            satisfaction=5
            )
        self.url = reverse('app:post_delete', args=[self.post.pk])

    def test_67_post_delete_by_owner(self):
        """
        投稿ユーザーにて、削除を実行した場合
        """
        self.client.login(
            email='main@test.com',
            password='testpassword1'
            )
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('app:post_list'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), '投稿を削除しました。')

        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(pk=self.post.pk)

    def test_68_post_delete_by_non_owner(self):
        """
        他のユーザーにて、削除を実行した場合
        """
        self.client.login(
            email='other@test.com',
            password='testpassword2'
            )
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('app:post_list'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'この投稿を削除する権限がありません。')

        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())

class MyPostListViewTests(TestCase):

    def setUp(self):
        self.main_user = User.objects.create_user(
            email='main@test.com',
            password='testpassword1'
            )
        self.other_user = User.objects.create_user(
            email='other@test.com',
            password='testpassword2'
            )
        self.url = reverse('app:post_mine')

        # Create posts for main_user
        for i in range(13):
            Post.objects.create(
                user=self.main_user,
                post_title=f'Test Title {i}',
                reason='Test Reason',
                impressions='Test Impressions',
                satisfaction=5
                )

        # Create posts for other_user
        for i in range(5):
            Post.objects.create(
                user=self.other_user,
                post_title=f'Other Title {i}',
                reason='Other Reason',
                impressions='Other Impressions',
                satisfaction=4
                )

    def test_69_get_queryset_only_request_user(self):
        """
        抽出したpostsがすべてログインユーザーのものか確認
        """
        self.client.login(
            email='main@test.com',
            password='testpassword1'
            )

        # 最初のページ
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        posts = response.context['posts']
        self.assertEqual(posts.count(), 5)
        for post in posts:
            self.assertEqual(post.user, self.main_user)

        # 2ページ目
        response = self.client.get(self.url + '?page=2')
        self.assertEqual(response.status_code, 200)
        posts = response.context['posts']
        self.assertEqual(posts.count(), 5)
        for post in posts:
            self.assertEqual(post.user, self.main_user)

        # 3ページ目（最後のページ）
        response = self.client.get(self.url + '?page=3')
        self.assertEqual(response.status_code, 200)
        posts = response.context['posts']
        self.assertEqual(posts.count(), 3)
        for post in posts:
            self.assertEqual(post.user, self.main_user)

    def test_70_get_queryset_not_logged_in_user(self):
        """
        ログインしていないユーザーにてアクセスした場合
        """
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{reverse('accounts:accounts_login')}?next={self.url}")
