from django.conf.urls import url
from django.contrib.auth import views as auth_views

from account.views import login, register, registration_complete, profile, myProfile, blockUser, edit_profile, email_verify
from account.forms import AuthenticationFormWithEmail

urlpatterns = [
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'account/logout.html', 'next_page': '/'}, name='logout'),
    url(r'^register/$', register, name='register'),
    url(r'^register/complete/$', registration_complete, name='registration_complete'),
    url(r'^profile/(?P<user_id>[0-9]+)/$', profile, name='profile'),
    url(r'^profile/$', myProfile, name='myProfile'),
    url(r'^edit_profile/$', edit_profile, name='edit_profile'),
    url(r'^block_user/(?P<user_id>[0-9]+)/$', blockUser, name='block_user'),
    url(r'^emailverify/(?P<token>.*)/$' , email_verify, name='email_verify'),
]

