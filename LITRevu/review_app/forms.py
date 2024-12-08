from django import forms
from .models import Ticket, Review
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        labels = {
            'title': 'Titre',
            'description': 'Description',
            'image': 'Image'
        }
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'headline', 'body']
        labels = {
            'rating': 'Note',
            'headline': 'Titre de la critique',
            'body': 'Critique'
        }
        widgets = {
            'rating': forms.RadioSelect(choices=[
                (0, '0'), 
                (1, '1'), 
                (2, '2'), 
                (3, '3'), 
                (4, '4'), 
                (5, '5')
            ]),
            'headline': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
