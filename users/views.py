from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from shopproject.settings import LOGIN_REDIRECT_URL
from .models import CustomUser
from users.forms import RegistrationForm, CustomPasswordChangeForm, LoginForm, ProfileForm


def register(request):
    # Когда отправляем форму на сервер
    if request.method == 'POST':
        print("POST data:", request.POST)  # данные формы
        print("FILES data:", request.FILES)
        # создаём объект формы с данными из запроса
        form = RegistrationForm(request.POST, request.FILES)
        print("Form is valid?", form.is_valid())  # <-- Отладка
        print(form.errors)
        # если форма валидна
        if form.is_valid():
            # создаём объект пользователя без записи в ДБ
            new_user = form.save(commit=False)
            # хешируем пароль
            new_user.set_password(form.cleaned_data['password'])
            # сохраняем пользователя в ДБ
            new_user.save()
            login(request, new_user)
            context = {'title':'Регистрация завершена', 'new_user': new_user}
            return render(request, template_name='users/registration_done.html', context=context)
    # Если метод GET (страница с пустой формой регистрации)
    form = RegistrationForm()
    context = {'title':'Регистрация пользователя', 'register_form': form}
    return render(request, template_name='users/registration.html', context=context)

def log_in(request):
    # создание формы
    form = LoginForm(request, request.POST)
    # проверка формы
    if form.is_valid():
        # получение логина и пароля формы
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        # аутентификация пользователя
        # проверка существования пользователя и корректности пароля
        user = authenticate(username=username, password=password)
        # если такой пользователь существует и пароль верный
        if user:
            # авторизация пользователя
            login(request, user)
            # получение дальнейшего маршрута после входа на сайт
            # next - путь, откуда пришёл пользователь на страницу входа
            url = request.GET.get('next', LOGIN_REDIRECT_URL)
            return redirect(url)
    context = {'form': form}
    return render(request, template_name='users/login.html', context=context)

@login_required
def log_out(request):
    logout(request)
    return redirect('shop:index')

@login_required
def user_profile(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.user != user:
        raise PermissionDenied()
    context = {'user': user, 'title': 'Информация о пользователе'}
    return render(request, template_name='users/profile.html', context=context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Ваш пароль успешно изменён')
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, 'users/change_password.html', {'form': form})

def change_profile(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save(request.user)
            messages.success(request, 'Данные успешно изменены')
    else:
        form = ProfileForm(initial={
            'username': user.username,
            'email': user.email,
            'image': user.image,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user.phone
        })
    return render(request, template_name='users/change_profile.html', context={'form': form})
