'''Файл со страницами'''
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import get_user_model, logout, login
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from .models import *
from .forms import *

def index(request):
    '''Стартовая страница'''
    logout(request)
    user = None
    return render(request, 'testblogapp/index.html', {'user':user})

def user_login(request):
    '''Страница входа в систему'''
    user = get_user_model()
    user_login_form = UserLogIn()
    if request.method == "POST":
        user_login_form = UserLogIn(data=request.POST)
        if user_login_form.is_valid():
            user_n = user_login_form.cleaned_data['username']
            password_n = user_login_form.cleaned_data['password']
        user_n = user_login_form['username'].value()
        password_n = user_login_form['password'].value()
        if not user.objects.filter(username = user_n, is_active = True).exists():
            m_error = "Нет такого пользователя!!! Зарегистрируйтесь пожалуйста."
            return render(request, 'testblogapp/user_error.html', {"m_error": m_error, 'p_activ': 2, })
        user = user.objects.get (username = user_n)
        if check_password(password_n, user.password):
            pass
        else:
            m_error = "Неверный пароль!!! Пожалуйста попробуйте еще раз."
            return render(request, 'testblogapp/user_error.html', {"m_error": m_error, 'p_activ': 2,})
        login(request, user)
        return redirect("testblogapp:str_user", permanent=True)
    else:
        val_data = {"form": user_login_form, }
        return render(request, 'testblogapp/user_login.html', val_data)

@login_required
def str_user(request):
    '''Страница пользователя'''
    user = request.user
    print(user)
    if request.method == "POST":
        req_post = request.POST
    else:
        val_data = {}
        return render(request, 'testblogapp/str_user.html', val_data)
