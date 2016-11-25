from django.contrib import admin

from forum.models import Question, Answer

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'published')


@admin.register(Answer)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('description', 'published')
