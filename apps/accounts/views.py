from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import StudentRegistrationForm, UserLoginForm

def register_view(request):
    if request.method == 'POST':
        # PASS THE DATA TO THE FORM
        form = StudentRegistrationForm(request.POST)
        
        # VALIDATE (Checks password strength & unique username)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = StudentRegistrationForm()

    # Pass 'form' to template so it displays specific errors
    return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Handle the 'next' url if it exists
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('home')
    else:
        form = UserLoginForm()

    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('accounts:login') 