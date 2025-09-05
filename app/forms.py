from django import forms
from django.contrib.auth.models import User
from . models import Comment, Blog_post

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name', 'last_name', 'email', 'username']

class Blogform(forms.ModelForm):
    class Meta:
        model=Blog_post
        fields=['title', 'content', 'tags', 'image']