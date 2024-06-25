from django.urls import path
from django.views.generic.base import TemplateView
from accounts.views import user_views

app_name = 'accounts'

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name="accounts_home"),
    path('signup/', user_views.SignupView.as_view(), name="accounts_signup"),
    path('login/', user_views.LoginView.as_view(), name="accounts_login"),
]
