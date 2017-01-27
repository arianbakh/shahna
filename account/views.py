from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth import views as auth_views
from django.http import HttpResponseRedirect, Http404
from django.views.decorators.http import require_POST
from django.shortcuts import render_to_response, render


from account.utils import make_thumbnail
from account.models import Profile, BlockUser
from account.forms import ProfileForm, BlockUserForm, UserCreationFormWithEmail, AuthenticationFormWithEmail


def login(request, template_name='account/login.html',
           redirect_field_name = '/profile/',
           authentication_form = AuthenticationFormWithEmail,
           extra_context=None):
    return auth_views.login(request, template_name, redirect_field_name,
                            authentication_form)


def register(request):
    if request.method == 'POST':
        user_form = UserCreationFormWithEmail(request.POST)
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
        user_form = UserCreationFormWithEmail()
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

    block_history = []
    blockUserForm = None
    if request.user and request.user.is_superuser:
        block_history = BlockUser.objects.filter(user=profile.user)
        blockUserForm = BlockUserForm()

    user_block = None
    if request.user == profile.user:
        user_block = BlockUser.objects.filter(user=request.user, unlimited=True).first()
        if not user_block:
            user_block = BlockUser.objects.filter(user=request.user, till_date__gt=datetime.now()). \
                order_by('-till_date').first()
    return render(request, 'account/profile.html', {'profile': profile, 'block_user_form': blockUserForm, \
                                                    'user_block': user_block, 'block_history':block_history})

def myProfile(request):
    if request.user != None:
        return HttpResponseRedirect('/accounts/profile/%d/' % request.user.id)
    return HttpResponseRedirect('/accounts/login/')

@require_POST
def blockUser(request, user_id):
    if request.user.is_superuser:
        block_user_form = BlockUserForm(request.POST)
        if block_user_form.is_valid():
            block = block_user_form.save(commit=False)
            duration = block_user_form.cleaned_data['block_time']
            if int(duration) == 0:
                block.till_date = datetime.now()
                block.unlimited = True
            else:
                block.till_date = datetime.now() + timedelta(days=int(duration))
            block.user = User.objects.get(id=user_id)
            block.save()
        return HttpResponseRedirect(reverse('profile', kwargs={"user_id": user_id}) )
    else:
       raise Http404()
