from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import User


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        # checkbox 'is_instructor' decides role
        is_instructor = request.POST.get('is_instructor')
        role = 'instructor' if is_instructor else 'student'

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )
        login(request, user)
        return redirect('home')

    return render(request, 'auth/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('home')

    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')
