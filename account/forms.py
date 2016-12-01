from django import forms

from account.models import User, Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'avatar', 'email', 'phone', 'city', 'university', 'current_work_place')
