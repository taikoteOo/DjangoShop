from datetime import date

from django import forms
from django.contrib.auth.forms import SetPasswordForm, AuthenticationForm
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
            'image': 'Фото профиля',
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

class CustomPasswordChangeForm(SetPasswordForm):
    odl_password = forms.CharField(
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
    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if  old_password and new_password1:
            if old_password == new_password1:
                raise ValidationError('Новый пароль должен отличаться от старого')

        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise ValidationError('Введённые пароли не совпадают')

        return cleaned_data

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