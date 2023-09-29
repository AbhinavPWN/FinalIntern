from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print('Registration complete')
            return render(request, 'auths/login.html')
    else:
        form = RegistrationForm()

    return render(request, 'auths/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully')
                print( 'Logged in successfully')
                # Store the user's username in the session
                # request.session['username'] = user.username
                username = user.username
                return render(request, 'home/index.html',{'username': username})
            else:
                messages.error(request, 'Authentication failed. Please check your credentials.')
        else:
            messages.error(request, 'Form is invalid. Please correct the errors.')

    else:
        print( 'Logged in unsuccessful')
        form = LoginForm()

    return render(request, 'auths/login.html', {'form': form})

@login_required
def user_logout(request):
    # Log the user out
    logout(request)
    # Redirect to the login page (you can customize the URL)
    return redirect('auths:login') 