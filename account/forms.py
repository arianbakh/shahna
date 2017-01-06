from django import forms
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from account.models import User, Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'nickname', 'avatar', 'email', 'phone', 'city', 'country', 'university', 'current_work_place', 'student_number',)
        widgets = {
                'student_number': forms.TextInput(attrs={'placeholder': _('Optional')}),
        }

    def clean_avatar(self):
        pic = self.cleaned_data['avatar']
        if pic._size > settings.MAX_UPLOAD_SIZE:
            raise ValidationError(_("Please keep filesize under %s.") % filesizeformat(settings.MAX_UPLOAD_SIZE))
        return pic
