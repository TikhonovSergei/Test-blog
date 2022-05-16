'''Файл со страницами'''
from datetime import date, time, datetime, timedelta
import os
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import get_user_model, logout, login
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *