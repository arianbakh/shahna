from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(verbose_name=_("Avatar"), upload_to='avatars/', max_length=255)
    name = models.CharField(verbose_name=_("Name"), max_length=15)
    nickname = models.CharField(verbose_name=_("Nickname (Display name)"), max_length=15)
    email = models.EmailField(verbose_name=_("Email"), max_length=50)
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


