from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile


def user_login(request):
    """Вход на сайт"""
    if request.method == 'POST':
        # Создаём объект формы с данными
        form = LoginForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # Сравниваем с даннми в БД
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    # Авторизуем пользователя на сайте и сохраняем его в сессии
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login or password')
    else:
        form = LoginForm()

    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        user_form = UserRegistrationForm(data=request.POST)
        if user_form.is_valid():
            # Создаём нового пользователя, но не сохраняем его в БД
            new_user = user_form.save(commit=False)
            # Задаём пользователю зашифрованный пароль т.е. сохраняем не напрямую код в БД
            new_user.set_password(user_form.cleaned_data['password'])
            # Сохраняем пользователя в БД
            new_user.save()
            # Создание профиля пользователя
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    """Редактирование профиля пользователя"""
    if request.method == 'POST':
        # instance=request.user - заполнить поля данными из БД
        # data=request.POST - записать данные из полей в БД
        # files=request.FILES - то же для медиа
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })
