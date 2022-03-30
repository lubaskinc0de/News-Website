import random
from uuid import uuid4
from django import forms
from .models import News,Comment,Code
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
import secrets
import string

class ContactForm(forms.Form):
    subject = forms.CharField(label='Вопрос',widget=forms.TextInput(attrs={'class':'form-control'}))
    body = forms.CharField(label='Описание вопроса',widget=forms.Textarea(attrs={'class':'form-control','rows':'5'}))
    


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя',widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='Пароль',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    code = forms.IntegerField(label='Ваш персональный код',help_text='При регистрации был выслан на ваш email',widget=forms.NumberInput(attrs={'class':'form-control'}))

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя',help_text='Имя пользователя должно быть уникальным',widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='Email',widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Пароль',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Подтвердите пароль',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = User
        fields = ('username','email','password1','password2')
    
    def clean_email(self):
        email_user = self.cleaned_data['email']
        if User.objects.filter(email=email_user).exists():
            raise ValidationError('Такой email уже существует.')
        return email_user

    def clean_username(self):
        username_user = self.cleaned_data['username']
        if Code.objects.filter(user_name=username_user).exists():
            raise ValidationError('Такое имя пользователя уже зарезервировано')
        return username_user


class NewsForm(forms.ModelForm): # создаем форму
    #форма добавления новостей
    class Meta:
        model = News # связываем с классом
        #fields = '__all__' # все поля
        fields = ['title','content','is_published','category']
        widgets = { 
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class':'form-control','rows':'5'}),
            'category': forms.Select(attrs={'class':'form-select'}),
            'is_published': forms.CheckboxInput(attrs={'class':'form-check-input'})
            } 
# добавляем красоту в форму черещ виджет
    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d',title): # если начинаеться с цифры # валиид
            raise ValidationError('First the paper symbol must not start with a digit')
        return title

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body':forms.Textarea(attrs={'class':'form-control','rows':3})
        }

