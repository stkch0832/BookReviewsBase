from allauth.account.forms import (
    SignupForm,
    LoginForm,
    ResetPasswordForm,
    ResetPasswordKeyForm,
    ChangePasswordForm,
    SetPasswordForm,
)
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomSignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)

        self.fields['password1'] = forms.CharField(
            label='パスワード',
            widget=forms.PasswordInput(),
            )

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control mb-3'

        for field in self.fields.values():
            field.widget.attrs['placeholder'] = ''

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('このメールアドレスは既に登録されています。')
        return email


class CustomLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)

        self.fields['login'].widget.attrs['class'] = 'form-control mb-3'
        self.fields['password'].widget.attrs['class'] = 'form-control mb-3'

        for field in self.fields.values():
            field.widget.attrs['placeholder'] = ''


class CustomResetPasswordForm(ResetPasswordForm):

    def __init__(self, *args, **kwargs):
        super(CustomResetPasswordForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        for field in self.fields.values():
            field.widget.attrs['placeholder'] = ''


class CustomResetPasswordKeyForm(ResetPasswordKeyForm):

    def __init__(self, *args, **kwargs):
        super(CustomResetPasswordKeyForm, self).__init__(*args, **kwargs)

        self.fields['password1'] = forms.CharField(
            label='パスワード',
            widget=forms.PasswordInput(),
            )

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        for field in self.fields.values():
            field.widget.attrs['placeholder'] = ''


class CustomChangePasswordForm(ChangePasswordForm):

    def __init__(self, *args, **kwargs):
        super(CustomChangePasswordForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        for field in self.fields.values():
            field.widget.attrs['placeholder'] = ''


class CustomSetPasswordForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super(CustomSetPasswordForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        for field in self.fields.values():
            field.widget.attrs['placeholder'] = ''
