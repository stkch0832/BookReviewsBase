from django import forms
from django.contrib.auth import get_user_model
from app.models.post_models import Post


User = get_user_model()

SATISFACTION_CHOICES = [
    ( '', '------ 選択してください ------'),
    ( 5, '5. とても満足' ),
    ( 4, '4. やや満足' ),
    ( 3, '3. どちらともいえない' ),
    ( 2, '2. あまり満足できなかった' ),
    ( 1, '1. 全く満足できなかった' ),
]

class PostForm(forms.ModelForm):
    impressions = forms.CharField(
        label='所感',
        max_length=255,
        widget=forms.Textarea()
    )
    satisfaction = forms.ChoiceField(
        label='満足度',
        choices=SATISFACTION_CHOICES,
    )

    book_title_display = forms.CharField(
        label='本のタイトル',
        required=False,
        disabled=True
        )
    author_display = forms.CharField(
        label='著者名',
        required=False,
        disabled=True
        )
    isbn_display = forms.CharField(
        label='ISBNコード',
        required=False,
        disabled=True
        )

    def __init__(self, *args, **kwargs):
        book_data = kwargs.pop('book_data', {})
        super(PostForm, self).__init__(*args, **kwargs)

        if book_data:
            self.fields['book_title_display'].initial = book_data.get('title')
            self.fields['author_display'].initial = book_data.get('author')
            self.fields['isbn_display'].initial = book_data.get('isbn')

        self.fields['post_title'].widget.attrs['placeholder'] = '25文字以内'
        self.fields['reason'].widget.attrs['placeholder'] = '25文字以内'
        self.fields['impressions'].widget.attrs['placeholder'] = '25文字以内'

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control mb-3'

    class Meta:
        model = Post
        fields = [
            'post_title',
            'reason',
            'impressions',
            'satisfaction',
        ]
