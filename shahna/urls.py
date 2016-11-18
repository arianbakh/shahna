from django.conf.urls import url
from django.contrib import admin

from core.views import home, login, logout, profile


urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^admin/', admin.site.urls),
]
