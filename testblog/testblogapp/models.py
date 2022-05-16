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
