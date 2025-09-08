from django import forms
from .models import BookReview, CustomUser, BookInstance
from django.contrib.auth.forms import UserCreationForm

class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['content']


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class BookInstanceCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ['book', 'due_back', 'reader', 'status']
        widgets = {'due_back': forms.DateInput(attrs={'type': 'date'})}