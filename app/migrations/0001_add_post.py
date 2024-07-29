# Generated by Django 4.2.13 on 2024-07-16 14:15

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_title', models.CharField(max_length=25, verbose_name='タイトル')),
                ('reason', models.CharField(max_length=25, verbose_name='動機・目的')),
                ('impressions', models.TextField(max_length=255, verbose_name='所感')),
                ('satisfaction', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='満足度')),
                ('book_title', models.CharField(max_length=255, verbose_name='本のタイトル')),
                ('author', models.CharField(max_length=255, verbose_name='著者名')),
                ('isbn', models.CharField(max_length=13, verbose_name='ISBNコード')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='登録日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'posts',
            },
        ),
    ]
