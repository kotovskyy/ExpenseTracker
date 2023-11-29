from django.shortcuts import render
from .forms import (SignupForm)

def userLogin(request):
    if request.method == 'POST':
        pass
    return render(request, 'users/login.html')

def userSignUp(request):
    if request.method == 'POST':
        pass
    form = SignupForm()
    return render(request, 'users/signup.html', context={
        'form': form,
    })

