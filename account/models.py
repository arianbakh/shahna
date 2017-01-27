from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from forum.models import UniversityField

def _avatar_file_name(instance, filename):
    format = filename
    splited = filename.split('.')
    if len(splited) > 1:
        format = '.' + splited[-1]
    return '/'.join(['avatars', instance.user.username+format])

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(verbose_name=_("Avatar"), upload_to=_avatar_file_name, max_length=255)
    name = models.CharField(verbose_name=_("Name"), max_length=15)
    nickname = models.CharField(verbose_name=_("Nickname (Display name)"), max_length=15)
    phone = models.CharField(verbose_name=_("Mobile phone"), max_length=15)
    city = models.CharField(verbose_name=_("Current city"), max_length=15)
    country = models.CharField(verbose_name=_("Current country"), max_length=15)
    university = models.CharField(verbose_name=_("Graduated university"), max_length=50)
    current_work_place = models.CharField(verbose_name=_("Current work place"), max_length=50)
    student_number = models.PositiveIntegerField(verbose_name=_("Student number"), blank=True, null=True)
    stars = models.PositiveIntegerField(verbose_name=_("Stars"), default=0)
    USER_STATE_CHOICES = (
        ('N', _("New")),
        ('J', _("Rejected")),
        ('A', _("Accepted")),
    )
    access_level = models.CharField(verbose_name=_("User access level"), max_length=1,
                                             choices=USER_STATE_CHOICES)
    university_field = models.ForeignKey(UniversityField, verbose_name=_("Field"))

    def change_star(self, count):
        '''
        :param count: Number of stars (can be negative and reduce stars)
        :return: Nothing
        '''
        if self.stars + count >= 0:
            self.stars += count
            self.save()
        else:
            self.stars = 0
            self.save()

class BlockUser(models.Model):
    user = models.ForeignKey(User)
    reason = models.TextField(verbose_name=_("Block reason"), default="", blank=True, null=True)

    DURATION_CHOICES = (
        (0, _("Unlimited")),
        (1, _("1 Day")),
        (3, _("3 Days")),
        (7, _("7 Days")),
    )
    till_date = models.DateTimeField(verbose_name=_("Block till"))
    unlimited = models.BooleanField(default=False)

