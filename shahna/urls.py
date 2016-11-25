from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from forum.views import home, ask, question_page


urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^ask/$', ask, name='ask'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('account.urls')),
    url(r'^question/(?P<question_id>[0-9]+)/$', question_page, name='question_page')
]
