from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *


# Create your views here.

# Login view function
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('music:index')
                else:
                    return HttpResponse("User is not active")
            else:
                messages.error(request, 'Incorrect username or password')
                return redirect('accounts:login_view')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


# SIGNUP VIEW FUNCTION
def signup_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('accounts:login_view')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/signup.html', {'form': form})


# Logout view function
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('accounts:login_view')
