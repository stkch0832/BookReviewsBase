from accounts.models.profile_models import Profile

def common(request):
    profile_data = None
    if request.user.is_authenticated:
        try:
            profile_data = Profile.objects.get(pk=request.user.id)
        except Profile.DoesNotExist:
            profile_data = None

    return {
        'profile_data': profile_data
    }
