from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .forms import (SignupForm)
from .models import User

def userLogin(request):
    if request.method == 'POST':
        email_or_username = request.POST["email_or_username"]
        password = request.POST["password"]
        try:
            username = User.objects.get(email=email_or_username)
        except User.DoesNotExist:
            username = email_or_username
            
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('core_index'))
        else:
            return render(request, "users/login.html", context={
                "message": "Invalid username or password",
            }) 
            
    return render(request, 'users/login.html')


def userSignUp(request):
    if request.method == 'POST':
        pass
    form = SignupForm()
    return render(request, 'users/signup.html', context={
        'form': form,
    })

