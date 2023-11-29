from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'core/index.html', context={
        "logged_in" : request.user.is_authenticated,
    })


@login_required
def categories(request):
    user = request.user
    categories = user.categories.filter(category_type='E').order_by('id')
    return render(request, 'core/categories.html', context={
        'categories': categories,
    })

