from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django.contrib.auth import get_user_model
from .models.profile_models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    readonly_fields = ('age',)
    extra = 0
    max_num = 1
    can_delete = False

    fieldsets = (
        (None, {
            'fields': (
                'username',
                'name',
                'introduction',
                'image',
                'bio',
                'birth',
                'age',
                'workplace',
                'occapation',
                'industry',
                'position',
                )
        }),
    )

class UserModelAdmin(UserAdmin):
    list_display = ("email", "is_active", "last_login", "created_at")
    list_filter = ("is_active", "is_staff")
    search_fields = ("email",)
    list_per_page = 20
    ordering = ("created_at",)
    fieldsets = (
        ('ユーザー情報', {'fields': ('email','password',)}),
        ('権限付与', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        ('ユーザー情報', {
            'fields': ('email','password1', 'password2')
        }),
        ('権限付与', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    inlines = [ProfileInline]

    def get_inline_instances(self, request, obj=None):
        if obj is None:
            return []
        return super(UserModelAdmin, self).get_inline_instances(request, obj)

admin.site.register(get_user_model(), UserModelAdmin)
