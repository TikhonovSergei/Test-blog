'''Файл админки'''
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from datetime import date
from .models import *

admin.site.register(User, UserAdmin)