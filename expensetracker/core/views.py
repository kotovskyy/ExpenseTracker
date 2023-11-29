from django.shortcuts import render


def index(request):
    return render(request, 'core/index.html', context={
        "logged_in" : request.user.is_authenticated,
    })

