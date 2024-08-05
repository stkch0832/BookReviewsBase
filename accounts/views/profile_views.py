from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.contrib.auth import get_user_model
from accounts.models.profile_models import Profile
from accounts.forms.profile_forms import ProfileForm
from app.models.post_models import Post
from django.core.paginator import Paginator

User = get_user_model()

def custom_404(request, exception):
    return render(request, '404.html', status=404)


class ProfileDetailView(DetailView):

        def get(self, request, *args, **kwargs):
            profile = get_object_or_404(Profile, username=kwargs['username'])
            posts = Post.objects.filter(user_id=profile.user_id).order_by('updated_at')

            paginator = Paginator(posts, 5)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)

            return render(request, 'account/profile_detail.html', context={
                'profile': profile,
                'posts': posts,
                'page_obj': page_obj
            })

class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    context_object_name = 'profile'
    template_name = 'account/profile_form.html'

    def get_object(self, queryset=None):
        return Profile.objects.get(user_id=self.request.user.id )

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

    def get_success_url(self):
        messages.success(self.request, 'プロフィールを変更しました。')
        return reverse('accounts:profile_edit')
