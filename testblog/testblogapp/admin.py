'''Файл админки'''
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(User, UserAdmin)

@admin.register(Blogs)
class BlogsAdmin(admin.ModelAdmin):
    list_display = ("user", "name_blog",)

@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ("blog", "title_post", "date_time_add")

@admin.register(BlogUser)
class BlogUserAdmin(admin.ModelAdmin):
    list_display = ("blog", "user", "signed")

@admin.register(PostUser)
class PostUserAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "read")