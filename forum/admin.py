from django.contrib import admin

from forum.models import Question, Answer, Tag, Subject

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'user', 'published')
    search_fields = ('title', 'description', 'user__username', 'user__profile__name')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'description', 'user', 'published')
    search_fields = ('question__title', 'description', 'user__username', 'user__profile__name')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Subject)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
