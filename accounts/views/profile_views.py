from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import (
    FormMixin,
    UpdateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.contrib import messages

from django.contrib.auth import get_user_model
from accounts.models.profile_models import Profile
from accounts.forms.profile_forms import ProfileForm

User = get_user_model()


class ProfileDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Profile
    form_class = ProfileForm
    context_object_name = 'profile'
    template_name = 'account/profile.html'

    def get_object(self, queryset=None):
        return Profile.objects.get(user_id=self.request.user)


    def get_initial(self):
        profile = Profile.objects.get(user_id=self.request.user.id)
        initial = super().get_initial()
        initial.update({
            'username': profile.username,
            'name': profile.name,
            'introduction': profile.introduction,
            'bio': profile.bio,
            'birth': profile.birth,
            'workplace': profile.workplace,
            'occapation': profile.occapation,
            'industry': profile.industry,
            'position': profile.position,

            'image': profile.image,
        })
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['profile'] = self.get_object()
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'account/profile.html'
    success_url = reverse_lazy('accounts:profile_detail')

    def get_object(self):
        return Profile.objects.get(user_id=self.request.user)

    def form_valid(self, form):
        try:
            self.object = form.save()
            messages.success(self.request, "プロフィールを更新しました")
            return redirect(self.success_url)
        except ValidationError as e:
            form.add_error('username' ,'birth', e)
            return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "プロフィールの更新に失敗しました")
        return super().form_invalid(form)
