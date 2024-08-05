from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from app.models.comment_models import Comment
from app.forms.comment_forms import CommentForm
from app.models.post_models import Post


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def get(self, request, *args, **kwargs):
        return redirect('app:post_detail', pk=kwargs['pk'])

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST or None)
        post = get_object_or_404(Post, pk=kwargs['pk'])

        if comment_form.is_valid():
            comment_form.instance.user = request.user
            comment_form.instance.post_id = post.pk
            comment_form.save()
            messages.success(self.request, 'コメントを投稿しました。')
            return redirect('app:post_detail', pk=post.pk)
        else:
            messages.error(self.request, 'コメントの投稿に失敗しました。')
            return redirect('app:post_detail', pk=post.pk)


class CommentDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Comment
    pk_url_kwarg = 'comment_id'
    success_message = "コメントを削除しました。"

    def get_success_url(self):
        post_id = self.kwargs['pk']
        return reverse_lazy('app:post_detail', kwargs={'pk': post_id})

    def dispatch(self, request, *args, **kwargs):
        post_id = kwargs['pk']
        comment = self.get_object()
        if comment.user != request.user:
            messages.error(request, 'このコメントを削除する権限がありません。')
            return redirect('app:post_detail', pk=post_id)
        return super().dispatch(request, *args, **kwargs)
