from django import forms
from django.contrib.auth import get_user_model
from app.models.comment_models import Comment

User = get_user_model()

class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='コメント',
        widget=forms.Textarea(attrs={
            'class': 'form-control mb-3',
            'placeholder': '255文字以内',
            'rows': 6,
            'cols': 50,
        })
    )

    class Meta:
        model = Comment
        fields = ['comment',]
