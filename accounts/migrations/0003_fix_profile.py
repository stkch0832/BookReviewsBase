# Generated by Django 4.2.13 on 2024-07-31 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_add_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='introduction',
            field=models.TextField(blank=True, max_length=255, null=True, verbose_name='自己紹介'),
        ),
    ]
