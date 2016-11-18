from django.conf.urls import url
from django.contrib import admin

from forum.views import home, login, logout, profile, ask


urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^ask/$', ask, name='ask'),
    url(r'^admin/', admin.site.urls),
]
