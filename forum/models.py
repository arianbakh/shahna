from __future__ import unicode_literals
from datetime import datetime, date

from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.utils.translation import ugettext_lazy as _


class Tag(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=50)

    class Meta:
        verbose_name=_("Tag")
        verbose_name_plural=_("Tags")

    def __unicode__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=50)

    def get_as_tag(self):
        return self.name.replace(' ', '_')

    class Meta:
        verbose_name=_("Subject")
        verbose_name_plural=_("Subjects")

    def __unicode__(self):
        return self.name


class Question(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(verbose_name=_("Title"), max_length=50)
    description = models.TextField(verbose_name=_("Description"), default="")
    stars = models.ManyToManyField(User, verbose_name=_("Stars"), related_name='question_user_stars')
    views = models.PositiveIntegerField(verbose_name=_("Views"), default=0)
    PUBLISH_STATE_CHOICES = (
        ('N', _("New")),
        ('R', _("Removed")),
        ('J', _("Rejected")),
        ('P', _("Published")),
    )
    published = models.CharField(verbose_name=_("Publish state"), max_length=1,
                                             choices=PUBLISH_STATE_CHOICES)
    upload_time = models.DateTimeField(verbose_name=_("Upload time"), auto_now_add=True)
    tags = models.ManyToManyField(Tag, verbose_name=_("tags"))
    subjects = models.ManyToManyField(Subject, verbose_name=_("Subjects"))

    class Meta:
        verbose_name=_("Question")
        verbose_name_plural=_("Questions")

    def __unicode__(self):
        return self.title

@receiver(pre_delete, sender=Question)
def remove_stars(sender, instance, using, **kwargs):
    instance.user.profile.change_star(-1 * settings.STAR_RULES['ASKING_QUESTION'])


class Answer(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    description = models.TextField(verbose_name=_("Description"), default="")
    accepted = models.BooleanField(verbose_name=_("Accepted"), default=False)
    stars = models.ManyToManyField(User, verbose_name=_("Stars"), related_name='answer_user_stars')
    PUBLISH_STATE_CHOICES = (
        ('N', _("New")),
        ('R', _("Removed")),
        ('J', _("Rejected")),
        ('P', _("Published")),
    )
    published = models.CharField(verbose_name=_("Publish state"), max_length=1,
                                             choices=PUBLISH_STATE_CHOICES, default='N')
    upload_time = models.DateTimeField(verbose_name=_("Upload time"), default=datetime.now)
    class Meta:
        verbose_name=_("Answer")
        verbose_name_plural=_("Answers")

@receiver(pre_delete, sender=Answer)
def remove_stars(sender, instance, using, **kwargs):
    instance.user.profile.change_star(-1 * settings.STAR_RULES['ANSWERING'])
