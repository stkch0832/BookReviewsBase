from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .api_views import get_api_data
from app.models.post_models import Post
from app.forms.post_forms import PostForm
from app.models.comment_models import Comment
from app.forms.comment_forms import CommentForm


class PostListView(ListView):
    model = Post
    paginate_by = 5
    template_name = 'index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.all().order_by('-updated_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        posts = context['posts']
        for post in posts:
            post.satisfaction = int(post.satisfaction)

        context['posts'] = posts
        context['satisfaction_range'] = range(5)

        return context


class PostDetailView(DetailView):
    model = Post

    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(pk=kwargs['pk'])

        isbn = self.get_queryset().first().isbn
        params = {
            'isbn': isbn,
        }

        api_response = get_api_data(params)
        if api_response is None:
            return render(request, 'app/post_detail.html', {
                'post_data': post_data,
                'error_message': 'APIのリクエストに失敗しました。'
            })

        if not api_response:
            return render(request, 'app/post_detail.html', {
                'post_data': post_data,
                'error_message': '該当のデータがありません。'
            })

        items = api_response
        item = items[0]['Item']
        title = item['title']
        image = item['largeImageUrl']
        author = item['author']
        salesDate = item['salesDate']
        publisherName = item['publisherName']
        isbn = item['isbn']
        itemCaption = item['itemCaption']
        itemUrl = item['itemUrl']
        reviewAverage = item['reviewAverage']
        reviewCount = item['reviewCount']

        book_data = {
            'title': title,
            'image': image,
            'author': author,
            'salesDate': salesDate,
            'publisherName': publisherName,
            'isbn': isbn,
            'itemCaption': itemCaption,
            'itemUrl': itemUrl,
            'reviewAverage': reviewAverage,
            'reviewCount': reviewCount,
        }

        comment_list = Comment.objects.filter(post_id=kwargs['pk']).order_by('-created_at')
        page = request.GET.get('page', 1)
        paginator = Paginator(comment_list, 5)

        try:
            comment_data = paginator.page(page)
        except PageNotAnInteger:
            comment_data = paginator.page(1)
        except EmptyPage:
            comment_data = paginator.page(paginator.num_pages)

        comment_form = CommentForm()

        return render(request, 'app/post_detail.html', context={
            'post_data': post_data,
            'satisfaction_range': range(5),
            'satisfaction_int': int(post_data.satisfaction),
            'book_data': book_data,
            'comment_data': comment_data,
            'comment_form': comment_form
        })

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        post_data = Post.objects.filter(pk=pk)
        return post_data


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'app/post_form.html'
    form_class = PostForm

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        post_data = Post.objects.filter(pk=pk)
        return post_data

    def get_initial(self):
        initial = super().get_initial()
        post_data = self.get_queryset().first()

        if post_data:
            initial['book_title_display'] = post_data.book_title
            initial['author_display'] = post_data.author
            initial['isbn_display'] = post_data.isbn
        return initial

    def get_success_url(self):
        messages.success(self.request, '投稿内容を変更しました。')
        return reverse('app:post_detail', kwargs={'pk': self.kwargs['pk']})

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.user != request.user:
            messages.error(request, 'この投稿を編集する権限がありません。')
            return redirect('app:post_list')
        return super().dispatch(request, *args, **kwargs)


class PostCreateView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        isbn = self.kwargs['isbn']
        params = {
            'isbn': isbn,
        }

        api_response = get_api_data(params)
        if api_response is None:
            return render(request, 'app/book_form.html', {
                'error_message': 'APIのリクエストに失敗しました。'
            })

        if not api_response:
            return render(request, 'app/book_form.html', {
                'error_message': '該当のデータがありません。'
            })

        items = api_response[0]
        item = items['Item']
        title = item['title']
        author = item['author']
        isbn = item['isbn']
        image = item['largeImageUrl']

        book_data = {
            'title': title,
            'author': author,
            'isbn': isbn,
            'image': image,
        }

        form = PostForm(
            request.POST or None,
            initial={
                'book_title_display': book_data['title'],
                'author_display': book_data['author'],
                'isbn_display': book_data['isbn'],
            }
        )

        return render(request, 'app/post_form.html', context={
            'form': form,
            'book_data': book_data,

        })

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)
        book_data = {
            'book_title': form.data['book_title'],
            'author': form.data['author'],
            'isbn': form.data['isbn'],
        }

        if form.is_valid():
            post_data = Post()
            post_data.user = request.user
            post_data.post_title = form.cleaned_data['post_title']
            post_data.reason = form.cleaned_data['reason']
            post_data.impressions = form.cleaned_data['impressions']
            post_data.satisfaction = form.cleaned_data['satisfaction']
            post_data.book_title = book_data['book_title']
            post_data.author = book_data['author']
            post_data.isbn = book_data['isbn']
            post_data.save()
            messages.success(request, '新規投稿をしました。')
            return redirect('app:post_list')

        return render(request, 'app/post_form.html', context={
            'form': form,
            'book_data': book_data,
        })


class PostDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('app:post_list')
    success_message = "投稿を削除しました。"

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.user != request.user:
            messages.error(request, 'この投稿を削除する権限がありません。')
            return redirect('app:post_list')
        return super().dispatch(request, *args, **kwargs)


class MyPostListView(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 5
    template_name = 'index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).order_by('-updated_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
