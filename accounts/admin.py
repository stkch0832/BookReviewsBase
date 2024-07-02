from django.contrib import admin
from .models.user_models import User
from .models.profile_models import Profile

admin.site.register(User)
admin.site.register(Profile)
