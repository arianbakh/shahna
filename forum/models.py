from __future__ import unicode_literals
from datetime import date

from django.db import models

class Question(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(default="")
    stars = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    PUBLISH_STATE_CHOICES = (
        ('N', "New"),
        ('J', "Rejected"),
        ('P', "Published"),
    )
    published = models.CharField(verbose_name="publish state", max_length=1,
                                             choices=PUBLISH_STATE_CHOICES)
    upload_time = models.DateTimeField(verbose_name="upload time", default=date.today)

class Answer(models.Model):
    question = models.ForeignKey(Question)
    description = models.TextField(default="")
    accepted = models.BooleanField(default=False)
    PUBLISH_STATE_CHOICES = (
        ('N', "New"),
        ('J', "Rejected"),
        ('P', "Published"),
    )
    published = models.CharField(verbose_name="publish state", max_length=1,
                                             choices=PUBLISH_STATE_CHOICES, default='N')
