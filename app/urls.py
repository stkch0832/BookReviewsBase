from django.urls import path
from app.views.post_views import (
    PostListView,
    PostDetailView,
    PostUpdateView,
    PostCreateView,
    PostDeleteView,
    MyPostListView,
)
from app.views.comment_views import (
    CommentCreateView,
    CommentDeleteView,
)
from app.views.book_views import (
    BookSearchView,
)

app_name = 'app'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('posts/new/<str:isbn>/', PostCreateView.as_view(), name='post_new'),
    path('posts/', MyPostListView.as_view(), name='post_mine'),

    path('posts/<int:pk>/comment/', CommentCreateView.as_view(), name='comment_new'),
    path('posts/<int:pk>/comment/<int:comment_id>/delete/', CommentDeleteView.as_view(), name='comment_delete'),

    path('book/search/', BookSearchView.as_view(), name='book_search'),

    ]
