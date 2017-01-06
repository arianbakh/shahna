from django import forms
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import AdminDateWidget

from account.models import Profile, BlockUser

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'nickname', 'avatar', 'email', 'phone', 'city', 'country', 'university', 'university_field', \
                  'current_work_place', 'student_number',)
        widgets = {
                'student_number': forms.TextInput(attrs={'placeholder': _('Optional')}),
        }

    def clean_avatar(self):
        pic = self.cleaned_data['avatar']
        if pic._size > settings.MAX_UPLOAD_SIZE:
            raise ValidationError(_("Please keep filesize under %s.") % filesizeformat(settings.MAX_UPLOAD_SIZE))
        return pic


class BlockUserForm(forms.ModelForm):
    block_time = forms.ChoiceField(choices=BlockUser.DURATION_CHOICES)
    class Meta:
        model = BlockUser
        fields = ('reason',)
