from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json
from shopproject.settings import LOGIN_REDIRECT_URL
from .models import CustomUser
from users.forms import RegistrationForm, CustomPasswordChangeForm, LoginForm, ProfileForm


@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            # 1. Получаем JSON из тела запроса
            data = json.loads(request.body)

            # 2. Передаём данные в форму
            form = RegistrationForm(data)

            # 3. Проверяем валидность
            if form.is_valid():
                # 4. Сохраняем пользователя
                user = form.save()  # пароль уже хешируется в save()

                # 5. Автоматически логиним
                login(request, user)

                # 6. Возвращаем успех + URL для перехода (если нужно)
                return JsonResponse({
                    'success': True,
                    'username': user.username,
                    'url': '/'  # можно изменить на profile или куда хочешь
                })

            else:
                # 7. Если ошибка — возвращаем ошибки формы
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                }, status=400)

        except Exception as e:
            # 8. Ошибка при разборе JSON или другая ошибка
            return JsonResponse({
                'success': False,
                'error': 'Некорректные данные'
            }, status=400)

    # Если GET — можно вернуть 405 (метод не поддерживается)
    return JsonResponse({'error': 'Метод не поддерживается'}, status=405)

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
    context = {'user': user, 'title': 'Информация о пользователе', 'is_profile_page': True}
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
    context = {'form': form, 'is_profile_page': True, 'is_profile_change': True}
    return render(request, 'users/change_password.html', context)

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
    context = {'form': form, 'is_profile_page': True, 'is_profile_change': True}
    return render(request, template_name='users/change_profile.html', context=context)
