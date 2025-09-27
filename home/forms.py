from django import forms
from utils.validation_utils import is_valid_email
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
        if not is_valid_email(email):
            raise forms.ValidationError("Invalid email format")
        return email

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message']


