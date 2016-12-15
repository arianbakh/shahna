from django import forms

from account.models import User, Profile
from django.utils.translation import ugettext_lazy as _

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'nickname', 'avatar', 'email', 'phone', 'city', 'country', 'university', 'current_work_place', 'student_number',)
        widgets = {
                'student_number': forms.TextInput(attrs={'placeholder': _('Optional')}),
        }
