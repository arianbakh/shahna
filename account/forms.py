from django import forms

from account.models import User, Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'email', 'phone', 'city', 'university', 'current_work_place')
