from django.shortcuts import render

def userLogin(request):
    if request.method == 'POST':
        pass
    return render(request, 'users/loginpage.html')

def userSignUp(request):
    if request.method == 'POST':
        pass
    return render(request, 'users/signup.html')


