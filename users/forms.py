from datetime import date

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.core.exceptions import ValidationError

from .models import CustomUser

class RegistrationForm(forms.ModelForm):
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'birthday', 'email', 'password')
        help_texts = {
            'username': ''
        }
        labels = {
            'birthday': 'Дата рождения'
        }
        widgets = {
            'birthday': forms.DateInput(attrs={'type':'date'}),
            'password': forms.PasswordInput()
        }

    def clean_password2(self):
        cleaned_data = self.cleaned_data
        if cleaned_data['password'] != cleaned_data['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return cleaned_data['password2']

    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')
        today = date.today()
        min_age_date = date(today.year - 18, today.month, today.day)

        if birthday and birthday > min_age_date:
            raise ValidationError("Вы должны быть старше 18 лет.")

        return birthday

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Старый пароль',
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'current-password', 'autofocus': True}
        ),
    )
    new_password1 = forms.CharField(
        label='Новый пароль',
        strip=False,
        widget=forms.PasswordInput()
    )
    new_password2 = forms.CharField(
        label='Подтверждение нового пароля',
        strip=False,
        widget=forms.PasswordInput()
    )

class LoginForm(AuthenticationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'password')
        help_texts = {
            'username': '',
            'password': ''
        }
        widgets = {
            'password': forms.PasswordInput()
        }

class ProfileForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'image',
            'first_name',
            'last_name',
            'phone'
        )
        labels = {
            'image': 'Фото профиля',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'phone': 'Номер телефона',
        }
        help_texts = {
            'username':'',
            'image': ''
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password')