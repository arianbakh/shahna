from __future__ import unicode_literals
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import translation
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from account.utils import random_key_generator, email_verification_days
from forum.models import UniversityField

def _avatar_file_name(instance, filename):
    format = filename
    splited = filename.split('.')
    if len(splited) > 1:
        format = '.' + splited[-1]
    return '/'.join(['avatars', instance.user.username+format])

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(verbose_name=_("Avatar"), upload_to=_avatar_file_name, \
            max_length=255, default="avatars/default.jpeg", blank=True, null=True)
    name = models.CharField(verbose_name=_("Name"), max_length=15, blank=True, null=True)
    nickname = models.CharField(verbose_name=_("Nickname (Display name)"), max_length=15, blank=True, null=True)
    phone = models.CharField(verbose_name=_("Mobile phone"), max_length=15, blank=True, null=True)
    city = models.CharField(verbose_name=_("Current city"), max_length=15, blank=True, null=True)
    country = models.CharField(verbose_name=_("Current country"), max_length=15, blank=True, null=True)
    university = models.CharField(verbose_name=_("Graduated university"), max_length=50, blank=True, null=True)
    current_work_place = models.CharField(verbose_name=_("Current work place"), max_length=50, blank=True, null=True)
    student_number = models.PositiveIntegerField(verbose_name=_("Student number"), blank=True, null=True)
    stars = models.PositiveIntegerField(verbose_name=_("Stars"), default=0)
    USER_STATE_CHOICES = (
        ('N', _("New")),
        ('J', _("Rejected")),
        ('A', _("Accepted")),
    )
    access_level = models.CharField(verbose_name=_("User access level"), max_length=1,
                                             choices=USER_STATE_CHOICES)
    university_field = models.ForeignKey(UniversityField, verbose_name=_("Field"), blank=True, null=True)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

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

class NewUser(models.Model):
    user = models.ForeignKey(User)
    code_creation_date = models.DateTimeField(default=datetime.now)
    verification_key = models.CharField(_('verification key'), max_length=40, default='')

    class Meta:
        verbose_name = _('New user email')
        verbose_name_plural = _('New user emails')

    def make_new_key(self):
        self.verification_key = random_key_generator(self.user.username)
        self.code_creation_date = datetime.now()

    def send_verification_email(self, lang):
        current_site = Site.objects.get_current()

        subject = render_to_string('account/verification_email_subject.txt',
            {'site': current_site})
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())

        expiration_days = email_verification_days()
        if lang == 'fa':
            expiration_days = expiration_days
        ctx = {'verification_key': self.verification_key,
               'expiration_days': expiration_days,
               'site': current_site,
               'first_email': True,
               'lang': lang}

        translation.activate(lang)
        message_txt = render_to_string('account/verification_email.txt', ctx)
        message_html = render_to_string('account/verification_email.html', ctx)

        msg = EmailMultiAlternatives(subject, message_txt,
                                     'test@test.com', [self.user.email])
        msg.attach_alternative(message_html, "text/html")
        msg.send()

    def verification_key_expired(self):
        if self.verification_key == None or self.verification_key == '':
            return True
        expiration_date = datetime.timedelta(days=email_verification_days())
        return self.code_creation_date + expiration_date <= datetime.now()

    def verify(self):
        self.user.is_active = True
        self.user.save()

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

    class Meta:
        verbose_name = _("User Block")
        verbose_name_plural = _("User Blocks")
