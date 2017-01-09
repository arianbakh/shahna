from django.conf import settings
from django.contrib import admin
from django.conf.urls import url, include, patterns
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView


from forum.views import home, ask, question_page, edit_question, remove_question, star_question, unstar_question, \
    edit_answer, remove_answer, accept_answer, reject_answer, star_answer, unstar_answer, search, tags, fields, new_answer

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^ask/$', ask, name='ask'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('account.urls')),
    url(r'^question/(?P<question_id>[0-9]+)/$', question_page, name='question_page'),
    url(r'^edit_question/(?P<question_id>[0-9]+)/$', edit_question, name='edit_question'),
    url(r'^remove_question/(?P<question_id>[0-9]+)/$', remove_question, name='remove_question'),
    url(r'^star_question/(?P<question_id>[0-9]+)/$', star_question, name='star_question'),
    url(r'^unstar_question/(?P<question_id>[0-9]+)/$', unstar_question, name='unstar_question'),
    url(r'^new_answer/(?P<question_id>[0-9]+)/$', new_answer, name='new_answer'),
    url(r'^edit_answer/(?P<answer_id>[0-9]+)/$', edit_answer, name='edit_answer'),
    url(r'^remove_answer/(?P<answer_id>[0-9]+)/(?P<question_id>[0-9]+)/$', remove_answer, name='remove_answer'),
    url(r'^accept_answer/(?P<answer_id>[0-9]+)/$', accept_answer, name='accept_answer'),
    url(r'^reject_answer/(?P<answer_id>[0-9]+)/$', reject_answer, name='reject_answer'),
    url(r'^star_answer/(?P<answer_id>[0-9]+)/$', star_answer, name='star_answer'),
    url(r'^unstar_answer/(?P<answer_id>[0-9]+)/$', unstar_answer, name='unstar_answer'),
    url(r'^search/?$', search, name='search'),
    url(r'^tags/(?P<tag_id>[0-9]+)/?$', tags, name='tags'),
    url(r'^fields/(?P<field_id>[0-9]+)/?$', fields, name='fields'),
    url(r'^about_us/$', TemplateView.as_view(template_name='about_us.html')),
]

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
