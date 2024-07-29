from django.urls import path
from django.views.generic.base import TemplateView
from accounts.views import user_views, profile_views

app_name = 'accounts'

urlpatterns = [
    path('signup/', user_views.SignupView.as_view(), name="accounts_signup"),
    path('login/', user_views.LoginView.as_view(), name="accounts_login"),

    path('profile/', profile_views.ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/edit/', profile_views.ProfileUpdateView.as_view(), name='profile_edit'),
]
