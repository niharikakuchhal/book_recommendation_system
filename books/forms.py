from django import forms
from django.contrib.auth.models import User
from .models import Recommendation, Comment

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

class RecommendationForm(forms.ModelForm):
    class Meta:
        model = Recommendation
        fields = ['book_title', 'book_description', 'author', 'link', 'cover_image', 'category', 'publication_date', 'rating']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
