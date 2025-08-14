from django import forms
from .models import feedbck


class feedbckForm(forms.ModelForm):
    class Meta:
        model = feedbck
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': 'Enter your feedback...','rows':4,'col':50}),
        }