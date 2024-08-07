from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.db.models import fields
from .models import Profile
from cloudinary.forms import CloudinaryFileField

class UserRegisterForm(UserCreationForm):
    email = models.EmailField()
    city = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
       
        ordered_fields = ['username', 'email', 'city', 'password1', 'password2']
        self.fields = {k: self.fields[k] for k in ordered_fields if k in self.fields}
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile = Profile(user=user, city=self.cleaned_data['city'])  # Save the city in Profile
            profile.save()
        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    image = CloudinaryFileField()
    class Meta:
        model = Profile
        fields = ['bio', 'city', 'image']
