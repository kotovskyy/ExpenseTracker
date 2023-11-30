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
    
@login_required
def accounts(request):
    user = request.user
    accounts = user.accounts.all().order_by('id')
    return render(request, 'core/accounts.html', context={
        'accounts': accounts,
    })
    
@login_required
def transactions(request):
    user = request.user
    transactions = user.transactions.all().order_by('id')
    return render(request, 'core/transactions.html', context={
        'transactions': transactions,
    })

@login_required
def category(request, category_id):
    user = request.user
    return render(request, 'core/category.html', context={
        
    })