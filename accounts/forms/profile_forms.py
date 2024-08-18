from django import forms
from accounts.models.profile_models import Profile
from django.core.validators import RegexValidator
from datetime import date
import re


class ProfileForm(forms.ModelForm):
    username = forms.CharField(
        max_length=30,
        min_length=5,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9\_]+$',
                message='半角英字(小文字・大文字)、数字、アンダースコア(_)を組み合わせて作成してください。'
        )],
        label='ユーザーID',
        required=True,
        help_text =[
            '5～30文字以内、半角英字(小文字・大文字)、数字、アンダースコア(_)のみ使用可能',
            ]
        )

    name = forms.CharField(
        max_length=30,
        label='名前',
        required=True,
        help_text =[
            '30文字以内'
        ]
    )

    introduction = forms.CharField(
        max_length=255,
        label='自己紹介',
        required=False,
        widget=forms.Textarea(),
        help_text =['255文字以内']
    )

    birth = forms.DateField(
        label='生年月日',
        required=False,
        widget=forms.NumberInput(attrs={
            'type': 'date',
        })
    )

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control mb-3'

    def clean_username(self):
        username = self.cleaned_data.get('username')

        existing_username = self.instance.username if self.instance else None

        if username != existing_username:
            username_exists = Profile.objects.filter(username=username).exists()
            if username_exists:
                raise forms.ValidationError('このユーザーIDは、既に使用されています。')

        if not re.match(r'^[a-zA-Z0-9\_]+$', username):
            raise forms.ValidationError('半角英字(小文字・大文字)、数字、アンダースコア(_)を組み合わせて作成してください。')
        return username

    def clean_birth(self):
        birth = self.cleaned_data.get('birth')
        today = date.today()
        if birth is not None and birth >= today:
            raise forms.ValidationError ('正しい生年月日を入力してください。')

        return birth


    class Meta:
        model = Profile
        fields = [
            'username',
            'name',
            'bio',
            'birth',
            'workplace',
            'occapation',
            'industry',
            'position',
            'birth',
            'introduction',
            'image',
            ]
