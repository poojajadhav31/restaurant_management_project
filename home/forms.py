from django import forms
from .models import feedbck

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

class feedbckForm(forms.ModelForm):
    class Meta:
        model = feedbck
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': 'Enter your feedback...','rows':4,'col':50}),
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = feedback
        fields = ['name', 'feedback_text']
        widgets = {
            'name':forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter your name'}),
            'feedback_text': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Write your feddback'}),
        }