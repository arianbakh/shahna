from account.models import Profile
from persian_tools import convert_english_digits_to_persian


def profile_completion_processor(request):
    if not request.user.is_authenticated() or request.user.is_superuser:
        return {}
    profile = Profile.objects.get(user=request.user)
    user_should_fill_fields = ['avatar', 'name', 'phone', 'city', 'country', 'university', \
            'current_work_place', 'entrance_year', 'student_number', 'university_field']
    filled = 0
    for field in user_should_fill_fields:
        if field == 'avatar':
            if not getattr(profile, field) == 'avatars/default.jpeg':
                filled += 1
        else:
            if getattr(profile, field):
                filled += 1
    profile_completion = str(int(100.0 * filled / len(user_should_fill_fields)))
    return {'profile_completion': convert_english_digits_to_persian(profile_completion)}
