'''Файл моделей'''
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AbstractUser, BaseUserManager
'''
class MyUserManager(BaseUserManager):
    pass
'''
class User(User):

    def __str__(self):
        return f"{self.username}"

class Blogs(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, primary_key = True)
    name_blog = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name_blog}"

class Posts(models.Model):
    blog = models.ForeignKey(Blogs, on_delete=models.PROTECT)
    title_post = models.CharField(max_length=140)
    text_post = models.TextField(null=True, blank=True)
    date_time_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title_post

class BlogUser(models.Model):
    blog = models.ForeignKey(Blogs, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    signed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.blog}"

class PostUser(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.post}"

