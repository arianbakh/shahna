from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(_("name"), max_length=15)
    email = models.EmailField(max_length=50)
    phone = models.CharField(_("phone"), max_length=15)
    city = models.CharField(_("city"), max_length=15)
    university = models.CharField(max_length=50)
    current_work_place = models.CharField(max_length=50)
    stars = models.PositiveIntegerField(verbose_name=_("network mnc"), default=0)


