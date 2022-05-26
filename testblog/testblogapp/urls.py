"""scrining URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import  path
from django.conf.urls import  url
from . import views
from django.conf import settings
from rest_framework import routers


app_name = 'testblogapp'



urlpatterns = [
    path('', views.index, name='index'),
    url('user_login/$', views.user_login, name='user_login'),
    path('str_user', views.str_user, name='str_user'),
    path('str_blogs', views.str_blogs, name='str_blogs'),
    path('my_blog', views.my_blog, name='my_blog'),
    path('add_post', views.add_post, name='add_post'),
    path('post)view/<int:pk_post>/', views.post_view, name='post_view'),
]





