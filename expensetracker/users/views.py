from django.shortcuts import render
from .forms import (UserCreationForm)

def userLogin(request):
    if request.method == 'POST':
        pass
    form = UserCreationForm()
    return render(request, 'users/login.html', context={
        'form': form,
    })

def userSignUp(request):
    if request.method == 'POST':
        pass
    return render(request, 'users/signup.html')


