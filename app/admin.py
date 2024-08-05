from django.contrib import admin
from .models.post_models import Post
from .models.comment_models import Comment

admin.site.register(Post)
admin.site.register(Comment)
