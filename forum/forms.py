from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from forum.models import Question, Answer

class QuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['tags'].label = _("Tags")

    tags = forms.CharField(max_length=255, help_text=_("Please enter tags separated by space ( at least 3 tags)"))
    class Meta:
        model = Question
        fields = ('title', 'description', 'fields')
        widgets = {
                "fields": forms.CheckboxSelectMultiple(),
        }
        error_messages = {
            'fields': {
                'required': _("Select at least one field"),
            },
        }
        lables = {
                'tags': _('Tags'),
        }

    def clean_tags(self):
        data = self.cleaned_data['tags']
        tags = set(data.split(' '))
        if len(tags) < 3:
            raise ValidationError(_(u'Enter at least three diffrent tags'))
        data.replace('#', '')
        return data

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('description',)
