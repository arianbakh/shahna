from account.models import Profile


def _convert_english_int_to_persian(english_int):
    persian_string = u''
    for english_character in str(english_int):
        persian_string += unichr(ord(english_character) + 1728)
    return persian_string


def profile_completion_processor(request):
    if not request.user.is_authenticated() or request.user.is_superuser:
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
    profile_completion = int(100.0 * filled / len(user_should_fill_fields))
    return {'profile_completion': _convert_english_int_to_persian(profile_completion)}
