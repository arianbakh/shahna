from django.conf import settings
from django.contrib import admin
from django.conf.urls import url, include, patterns
from django.contrib.auth import views as auth_views

from forum.views import home, ask, question_page, edit_question, remove_question, edit_answer, remove_answer


urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^ask/$', ask, name='ask'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('account.urls')),
    url(r'^question/(?P<question_id>[0-9]+)/$', question_page, name='question_page'),
    url(r'^edit_question/(?P<question_id>[0-9]+)/$', edit_question, name='edit_question'),
    url(r'^remove_question/(?P<question_id>[0-9]+)/$', remove_question, name='remove_question'),
    url(r'^edit_answer/(?P<answer_id>[0-9]+)/$', edit_answer, name='edit_answer'),
    url(r'^remove_answer/(?P<answer_id>[0-9]+)/(?P<question_id>[0-9]+)/$', remove_answer, name='remove_answer'),
]

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
