from django import forms
from .models import feedbck

class ContactForm(forms.Form):
    name = forms.Charfield(max_length=100, required=True,widget=forms.TextInput(attrs={
        'placeholder': "Your Name"
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': "Your Email"
    }))
    message = forms.Charfield(
        required=False,
        widget = forms.Textarea(attrs={'rows':4, 'placeholder': 'Yuor message (optional)'}),
    )

class feedbckForm(forms.ModelForm):
    class Meta:
        model = feedbck
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': 'Enter your feedback...','rows':4,'col':50}),
        }