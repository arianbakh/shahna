from account.models import Profile

def profile_completion_processor(request):
    if not request.user.is_authenticated():
        return {}
    profile = Profile.objects.get(user=request.user)
    user_should_fill_fields = ['avatar', 'name', 'nickname', 'phone', 'city', 'country', 'university', \
            'current_work_place', 'student_number', 'university_field']
    filled = 0
    for field in user_should_fill_fields:
        if field == 'avatar':
            if not getattr(profile, field) == 'avatars/default.jpeg':
                filled += 1
        else:
            if getattr(profile, field):
                filled += 1
    profile_completion = 100.0 * filled / len(user_should_fill_fields)
    return {'profile_completion': profile_completion}
