from accounts.forms.user_forms import (
    CustomSignupForm,
    CustomLoginForm,
    )
from allauth.account.views import (
    SignupView,
    LoginView,
    )


class SignupView(SignupView):
    template_name = 'account/signup.html'
    form_class = CustomSignupForm


class LoginView(LoginView):
    template_name = 'account/login.html'
    form_class = CustomLoginForm
