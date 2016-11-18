from __future__ import unicode_literals

from django.db import models

class Question(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(default="")
    stars = models.PositiveIntegerField(default=0)


class Answer(models.Model):
    question = models.ForeignKey(Question)
    description = models.TextField(default="")
    accepted = models.BooleanField(default=False)

