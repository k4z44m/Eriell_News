from django import forms
from .models import Article, Comment, Profile
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from simplemathcaptcha.fields import MathCaptchaField


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image', 'category']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control shadow',
                'placeholder': 'write text'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control shadow'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control shadow'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control shadow'
            })
        }


class LoginFrom(AuthenticationForm):
    username = forms.CharField(label="LOGIN", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="PASSWORD", widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))
    captcha = MathCaptchaField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'captcha']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'})
        }


class ProfileForm(forms.ModelForm):
    bio = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control'
        }))
    photo = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-control'
    }))
    instagram_url = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control'
        }))
    telegram_url = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control'
        }))
    facebook_url = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control'
        }))
    youtube_url = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control'
        }))

    class Meta:
        model = Profile
        fields = ['bio',
                  'photo',
                  'instagram_url',
                  'telegram_url',
                  'facebook_url',
                  'youtube_url'
                  ]

