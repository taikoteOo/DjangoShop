from users.forms import RegistrationForm
from django.http.response import JsonResponse, HttpResponse


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
    return JsonResponse(response_data)
