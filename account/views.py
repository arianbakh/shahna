from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings


from account.forms import ProfileForm
from account.models import Profile
from account.utils import make_thumbnail

def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.avatar = profile_form.cleaned_data['avatar']
            make_thumbnail(settings.MEDIA_ROOT + 'avatars/' + profile.user.username)
            profile.save()
            return HttpResponseRedirect('/accounts/register/complete')
    else:
        user_form = UserCreationForm()
        profile_form = ProfileForm()
    return render(request, 'register/registration_form.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def registration_complete(request):
    return render_to_response('register/registration_complete.html')


def profile(request, user_id):
    try:
        profile = Profile.objects.get(user__id=user_id)
    except Profile.DoesNotExist:
        raise Http404()
    return render(request, 'account/profile.html', {'profile': profile})

def myProfile(request):
    if request.user != None:
        return HttpResponseRedirect('/accounts/profile/%d/' % request.user.id)
    return HttpResponseRedirect('/accounts/login/')

