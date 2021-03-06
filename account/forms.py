from django import forms
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from account.models import Profile, BlockUser

class UserCreationFormWithEmail(UserCreationForm):
    username = forms.EmailField(max_length=64, label=_("Email"), help_text=_("Email Address"))
    i_agree = forms.BooleanField(label=_("I Agree with the terms and conditions"), required=False)

    def clean_email(self):
        email = self.cleaned_data['username']
        return email

    def clean_i_agree(self):
        i_agree = self.cleaned_data['i_agree']
        if not i_agree:
            raise ValidationError(_("You must accept our terms"))
        return i_agree


class AuthenticationFormWithEmail(AuthenticationForm):
    username = forms.EmailField(max_length=64, label=_("Email"), help_text=_("Email Address"))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'avatar', 'phone', 'city', 'country', 'university', 'university_field', \
                  'current_work_place', 'entrance_year', 'student_number',)
        widgets = {
                'entrance_year': forms.TextInput(attrs={'placeholder': _('1380')}),
                'student_number': forms.TextInput(attrs={'placeholder': _('88102030')}),
                'phone': forms.TextInput(attrs={'placeholder': _('02187654321')}),
                'avatar': forms.FileInput(),
        }

    def clean_avatar(self):
        pic = self.cleaned_data['avatar']
        if pic.size > settings.MAX_UPLOAD_SIZE:
            raise ValidationError(_("Please keep filesize under %s.") % filesizeformat(settings.MAX_UPLOAD_SIZE))
        return pic


class BlockUserForm(forms.ModelForm):
    block_time = forms.ChoiceField(choices=BlockUser.DURATION_CHOICES)
    class Meta:
        model = BlockUser
        fields = ('reason',)
