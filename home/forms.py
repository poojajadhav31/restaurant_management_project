from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Feedback

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True,widget=forms.TextInput(attrs={
        'placeholder': "Your Name"
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': "Your Email"
    }))
    message = forms.CharField(
        required=True,
        widget = forms.Textarea(attrs={'rows': 4, 'placeholder': 'Your message (optional)'}),
    )
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Invalid email format")
        return email
        return email

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message']


