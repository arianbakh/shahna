from django.contrib import admin

from forum.models import Question, Answer, Tag, Subject

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'published')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('description', 'published')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Subject)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
