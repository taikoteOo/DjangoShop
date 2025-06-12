from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.core.exceptions import ValidationError

from .models import CustomUser

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'birthday', 'city', 'image')
        help_texts = {
            'username': ''
        }

    def clean_password2(self):
        cleaned_data = self.cleaned_data
        if cleaned_data['password'] != cleaned_data['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return cleaned_data['password2']

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
        label='Подтвержение нового пароля',
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