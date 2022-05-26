'''Файл со страницами'''
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
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
        if Blogs.objects.filter(user = user).exists() == False:
            blog = Blogs(user = user, name_blog = 'Блог тест '+str(user.pk))
            blog.save()
        return redirect("testblogapp:str_user", permanent=True)
    else:
        val_data = {"form": user_login_form, }
        return render(request, 'testblogapp/user_login.html', val_data)

@login_required
def str_user(request):
    '''Страница пользователя'''
    user = request.user
    blog_my = Blogs.objects.get(user = user)
    blog_user_lst = Blogs.objects.filter(bloguser__user = user, bloguser__signed = True)
    post_lst = Posts.objects.filter(blog = blog_my)
    for blog_user in blog_user_lst:
        post_lst_add = Posts.objects.filter(blog = blog_user)
        post_lst = post_lst.union(post_lst_add)
    post_lst = post_lst.order_by('-date_time_add')
    if request.method == "POST":
        req_post = request.POST
        for key_post in req_post:
            if key_post.find('pk_') == 0:
                pk_post = int(key_post[3:])
                post = Posts.objects.get(pk = pk_post)
                if PostUser.objects.filter(user = user, post = post).exists() == False:
                    post_user = PostUser(user = user, post = post, read = True)
                    post_user.save()
                else:
                    post_user = PostUser.objects.get(user = user, post = post)
                    pk_post_user = post_user.pk
                    post_user.pk = pk_post_user
                    post_user.read = True
                    post_user.save()
            elif key_post.find('no_') == 0:
                pk_post = int(key_post[3:])
                post = Posts.objects.get(pk = pk_post)
                if PostUser.objects.filter(user = user, post = post).exists():
                    post_user = PostUser.objects.get(user = user, post = post)
                    pk_post_user = post_user.pk
                    post_user.pk = pk_post_user
                    post_user.read = False
                    post_user.save()
        return redirect('testblogapp:str_user', permanent=True)
    else:
        val_data = {'post_lst': post_lst,}
        return render(request, 'testblogapp/str_user.html', val_data)

@login_required
def my_blog(request):
    '''Страница своего блога пользователя'''
    user = request.user
    blog_my = Blogs.objects.get(user = user)
    post_lst = Posts.objects.filter(blog = blog_my)
    post_lst = post_lst.order_by('-date_time_add')
    val_data = {'post_lst': post_lst,}
    return render(request, 'testblogapp/my_blog.html', val_data)

@login_required
def add_post(request):
    '''Страница пользователя'''
    user = request.user
    blog_my = Blogs.objects.get(user = user)
    form_post = CreatePostForm()
    if request.method == "POST":
        form_post = CreatePostForm(request.POST)
        if form_post.is_valid():
            post = form_post.save(commit=False)
            post.blog = blog_my
            #post.date_time_add = datetime.today()
            post.save()
        return redirect('testblogapp:my_blog', permanent=True)
    else:
        val_data = {'form_post': form_post,}
        return render(request, 'testblogapp/add_post.html', val_data)

@login_required
def post_view(request, pk_post):
    '''Страница поста'''
    user = request.user
    try:
        post = Posts.objects.get(pk = pk_post)
    except ObjectDoesNotExist:
        m_error = "К сожалению пост не существует или удален"
        return render(request, 'testblogapp/user_error.html', {"m_error": m_error, 'p_activ': 2,})
    val_data = {'post': post,}
    return render(request, 'testblogapp/post.html', val_data)

@login_required
def str_blogs(request):
    '''Страница всех блогов'''
    user = request.user
    blog_lst = Blogs.objects.exclude(user = user)
    if request.method == "POST":
        req_post = request.POST
        for key_blog in req_post:
            if key_blog.find('pk_') == 0:
                pk_blog = int(key_blog[3:])
                blog = Blogs.objects.get(pk = pk_blog)
                if BlogUser.objects.filter(user = user, blog = blog).exists() == False:
                    blog_user = BlogUser(user = user, blog = blog, signed = True)
                    blog_user.save()
                else:
                    blog_user = BlogUser.objects.get(user = user, blog = blog)
                    pk_blog_user = blog_user.pk
                    blog_user.pk = pk_blog_user
                    blog_user.signed = True
                    blog_user.save()
            elif key_blog.find('no_') == 0:
                pk_blog = int(key_blog[3:])
                blog = Blogs.objects.get(pk = pk_blog)
                if BlogUser.objects.filter(user = user, blog = blog).exists():
                    blog_user = BlogUser.objects.get(user = user, blog = blog)
                    pk_blog_user = blog_user.pk
                    blog_user.pk = pk_blog_user
                    blog_user.signed = False
                    blog_user.save()
                post_lst = Posts.objects.filter(blog = blog)
                if len(post_lst) != 0:
                    for post in post_lst:
                        if PostUser.objects.filter(user = user, post = post).exists():
                            post_user = PostUser.objects.get(user = user, post = post)
                            pk_post_user = post_user.pk
                            post_user.pk = pk_post_user
                            post_user.read = False
                            post_user.save()
        return redirect('testblogapp:str_blogs', permanent=True)
    else:
        val_data = {'blog_lst': blog_lst,}
        return render(request, 'testblogapp/str_blogs.html', val_data)