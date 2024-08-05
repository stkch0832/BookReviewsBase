from django.db import models
from django.contrib.auth import get_user_model
from app.models.post_models import Post

User = get_user_model()

class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    comment = models.CharField(
        max_length=255,
        verbose_name='コメント'
        )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        verbose_name="登録日時",
        auto_now_add=True,
    )

    class Meta:
        db_table = 'comments'
        app_label = 'app'

    def __str__(self):
        return f'{self.user.profile.name} | {self.post.post_title}'
