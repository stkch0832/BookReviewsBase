from accounts.forms.user_forms import (
    CustomSignupForm,
    CustomLoginForm,
    )
from allauth.account.views import (
    SignupView,
    LoginView,
    )
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

User = get_user_model()

class SignupView(SignupView):
    template_name = 'account/signup.html'
    form_class = CustomSignupForm


class LoginView(LoginView):
    template_name = 'account/login.html'
    form_class = CustomLoginForm


class AccountDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'account/delete.html'
    success_url = reverse_lazy('app:post_list')
    success_message = "アカウントを削除しました。ご利用いただきありがとうございました。"

    def get_object(self):
        return self.request.user
