from __future__ import unicode_literals
from datetime import date

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Question(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(verbose_name=_("Title"), max_length=50)
    description = models.TextField(verbose_name=_("Description"), default="")
    stars = models.PositiveIntegerField(verbose_name=_("Stars"), default=0)
    views = models.PositiveIntegerField(verbose_name=_("Views"), default=0)
    PUBLISH_STATE_CHOICES = (
        ('N', "New"),
        ('J', "Rejected"),
        ('P', "Published"),
    )
    published = models.CharField(verbose_name=_("Publish state"), max_length=1,
                                             choices=PUBLISH_STATE_CHOICES)
    upload_time = models.DateTimeField(verbose_name=_("Upload time"), default=date.today)

class Answer(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    description = models.TextField(verbose_name=_("Description"), default="")
    accepted = models.BooleanField(verbose_name=_("Accepted"), default=False)
    PUBLISH_STATE_CHOICES = (
        ('N', "New"),
        ('J', "Rejected"),
        ('P', "Published"),
    )
    published = models.CharField(verbose_name=_("Publish state"), max_length=1,
                                             choices=PUBLISH_STATE_CHOICES, default='N')
