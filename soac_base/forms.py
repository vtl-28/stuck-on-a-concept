from .models import Answer
from django import forms

class CommentForm(forms.ModelForm):
    """
    class is a Django ModelForm that creates a form for the Comment
    widgets attribute, ensues they have the appropriate CSS
    classes ('form-control') for styling purposes.
    """
    class Meta:
        model = Answer
        fields = ['name', 'body']

        widgets = {
                'name': forms.TextInput(attrs={'class': 'form-control'}),
                'body': forms.TextInput(attrs={'class': 'form-control'}),
                }
