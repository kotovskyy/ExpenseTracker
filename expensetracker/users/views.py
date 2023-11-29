from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import (SignupForm)
from .models import User
from core.models import (Settings,
                         Category)

def userLogin(request):
    if request.method == 'POST':
        email_or_username = request.POST["email_or_username"]
        password = request.POST["password"]
        remember_me = request.POST.get('remember_me', False)
        try:
            username = User.objects.get(email=email_or_username)
        except User.DoesNotExist:
            username = email_or_username
            
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)
            
            return HttpResponseRedirect(reverse('core_categories'))
        else:
            return render(request, "users/login.html", context={
                "message": "Invalid username or password",
            }) 
        
    return render(request, 'users/login.html')


def userSignUp(request):
    BASE_CATEGORIES = ["Groceries", "Transport", "Home", "Clothes", "Health"]
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            settings = Settings.objects.create(
                user=user
            )
            for c in BASE_CATEGORIES:
                category = Category.objects.create(
                    user=user,
                    name=c
                )
            messages.success(request,"You have signed up successfully!")
            login(request, user)
            return HttpResponseRedirect(reverse('core_index'))
        else:
            return render(request, 'users/signup.html', context={
                'form': form,
            })
        
    form = SignupForm()
    return render(request, 'users/signup.html', context={
        'form': form,
    })
    
def userSignOut(request):
    logout(request)
    return HttpResponseRedirect(reverse('core_index'))

