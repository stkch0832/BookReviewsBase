from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


User = get_user_model()

class Post(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    post_title = models.CharField(
        max_length=25,
        verbose_name='タイトル'
        )
    reason = models.CharField(
        max_length=25,
        verbose_name='動機・目的'
    )
    impressions = models.CharField(
        max_length=255,
        verbose_name='所感'
    )
    satisfaction = models.PositiveIntegerField(
        verbose_name='満足度',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    book_title = models.CharField(
        max_length=255,
        verbose_name='本のタイトル'
        )
    author = models.CharField(
        max_length=255,
        verbose_name='著者名'
        )

    isbn = models.CharField(
        max_length=13,
        verbose_name='ISBNコード'
    )
    created_at = models.DateTimeField(
        verbose_name="登録日時",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name="更新日時",
        auto_now=True,
    )

    class Meta:
        db_table = 'posts'
        app_label = 'app'

    def __str__(self):
        return f'{self.post_title} | {self.user.profile.name} | {self.book_title}'
