from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
import uuid

# Create your views here.

@login_required
def home(request):
    return render(request, "auth/home.html")