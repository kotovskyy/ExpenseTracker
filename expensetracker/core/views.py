from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import (Currency,
                     Transaction,
                     Account,
                     Category)
from .forms import (AddNewAccountForm,
                    AddNewCategoryForm,
                    AddTransactionCategoryForm,
                    AddTransactionAccountForm,
                    EditCategoryForm,
                    EditAccountForm)

from decimal import Decimal
import datetime
import calendar

def convert_amount(amount, conv_from, conv_to):
    """
        Convert `amount` from `conv_from` currency to `conv_to` currency.
    """
    rate = conv_from.exchange_rates[conv_to.code]
    rate = Decimal(str(rate))
    return round(amount * rate, 2)

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('core_categories'))
        
    return render(request, 'core/index.html', context={
        "logged_in" : request.user.is_authenticated,
    })

@login_required
def categories(request):
    user = request.user
    main_currency = user.settings.first().main_currency
    categories = user.categories.filter(category_type='E').order_by('id')
    
        # get period of time (month) to filter data
    month_number = int(request.GET.get('month', datetime.date.today().month))
    year = int(request.GET.get('year', datetime.date.today().year))
    month_name = calendar.month_name[month_number]
    
    income_transactions = Transaction.objects.filter(
        user=user,
        date__month=month_number,
        date__year=year,
        transaction_type="I"
    )
    
    total_income = sum([convert_amount(t.amount, t.currency, main_currency) for t in income_transactions])
    
    categories_total = []
    
    for c in categories:
        total = 0
        transactions = c.transactions.filter(
            date__month=month_number,
            date__year=year
        )
        for t in transactions:
            total += convert_amount(t.amount, t.currency, main_currency)
        categories_total.append(total)
    
    total_expense = sum(categories_total)
    categories_expenses = list(zip(categories, categories_total)) 
    
    return render(request, 'core/categories.html', context={
        'categories': categories,
        "main_currency": main_currency,
        "total_expense": total_expense,
        "total_income": total_income,
        "month_name": month_name,
        "year":year,
        "categories_expenses" : categories_expenses,
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
    transactions = user.transactions.all().order_by('date').reverse()
    return render(request, 'core/transactions.html', context={
        'transactions': transactions,
    })

@login_required
def category(request, category_id):
    user = request.user
    category = user.categories.get(id=category_id)
    transactions = category.transactions.all().order_by('date').reverse()
    t_type = "E"
    if request.method == 'POST':
        form = AddTransactionCategoryForm(user, t_type, category_id, request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            date = form.cleaned_data["date"]
            description = form.cleaned_data["description"]
            account_id = form.cleaned_data["account"]
            currency_id = form.cleaned_data["currency"]
            account = user.accounts.get(id=account_id)
            currency = Currency.objects.get(id=currency_id)
            
            transaction = Transaction.objects.create(
                user=user,
                account=account,
                category=category,
                transaction_type=t_type,
                amount=amount,
                currency=currency,
                date=date,
                description=description
            )
            
            account.balance -= amount
            
            account.save()

        else:
            return render(request, 'core/category.html', context={
                "category": category,
                "form": form,
                'transactions' : transactions,
                'edit_form' : EditCategoryForm(user, category),
                'n_transactions': transactions.count(),
            })
            
    form = AddTransactionCategoryForm(user, t_type, category_id)
    edit_form = EditCategoryForm(user, category)
    return render(request, 'core/category.html', context={
        'form' : form,
        'category' : category,
        'transactions' : transactions,
        'edit_form' : edit_form,
        'n_transactions': transactions.count(),
    })
    
@login_required
def editCategory(request, category_id):
    user = request.user
    category = user.categories.get(id=category_id)
    if request.method == 'POST':
        form = EditCategoryForm(user, category, request.POST)
        if form.is_valid():
            new_name = form.cleaned_data['name']
            new_type = form.cleaned_data['category_type']
            
            category.name = new_name
            category.category_type = new_type
            
            category.save()
        else:
            return HttpResponseRedirect(reverse('core_category', args=(category_id,)))
    return HttpResponseRedirect(reverse('core_category', args=(category_id,)))

@login_required
def deleteCategory(request, category_id):
    user = request.user
    category = user.categories.get(id=category_id)
    main_currency = user.settings.get(user=user).main_currency
    transactions = category.transactions.all()
    if request.method == 'POST':
        for t in transactions:
            account = t.account
            amount = t.amount
            currency = t.currency
            amount_converted = convert_amount(amount, currency, main_currency)
            
            sign = -1 if t.transaction_type == "I" else 1
            
            account.balance += sign * amount_converted

            account.save()
            
            t.delete()
        
        category.delete()
        
    return HttpResponseRedirect(reverse('core_categories'))

@login_required
def addCategory(request):
    user = request.user
    if request.method == 'POST':
        form = AddNewCategoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            category_type = form.cleaned_data['category_type']
            
            category = Category.objects.create(
                user=user,
                name=name.capitalize(),
                category_type=category_type
            )
            
            return HttpResponseRedirect(reverse('core_categories'))
            
        else:
            return render(request, 'core/add_category.html', context={
                'form': form,
            })
        
    form = AddNewCategoryForm()
    return render(request, 'core/add_category.html', context={
        'form': form,
    })

@login_required
def account(request, account_id):
    user = request.user
    account = user.accounts.get(id=account_id)
    transactions = account.transactions.all().order_by('date').reverse()
    expense_categories = user.categories.filter(category_type="E").order_by('id')
    income_categories = user.categories.filter(category_type="I").order_by('id')
    transfer_accounts = user.accounts.all().exclude(id=account_id)
    t_types = ['E', 'I']
    options_by_type = {
        'E' : list(expense_categories),
        'I' : list(income_categories),
        'T' : list(transfer_accounts)
    }

    t_type = "E"
    edit_form = EditAccountForm(user, account)

    if request.method == 'POST':
        form = AddTransactionAccountForm(user, t_type, account_id, request.POST)
        if form.is_valid():
            t_type = form.cleaned_data['transaction_type']
            amount = form.cleaned_data["amount"]
            date = form.cleaned_data["date"]
            description = form.cleaned_data["description"]
            currency_id = form.cleaned_data["currency"]
            currency = Currency.objects.get(id=currency_id)
            category_id = form.cleaned_data["category"]
            category = user.categories.get(id=category_id)
        
            transaction = Transaction.objects.create(
                user=user,
                account=account,
                category=category,
                transaction_type=t_type,
                amount=amount,
                currency=currency,
                date=date,
                description=description
            )
            
            # expense
            if t_type == "E":
                account.balance -= amount
            if t_type == "I":
                account.balance += amount
        
            account.save()
            
        else:
            return render(request, 'core/account.html', context={
                't_types': t_types,
                'opt_by_type': options_by_type,
                'form' : form,
                'account' : account,
                'transactions' : transactions,
                'edit_form' : edit_form,
                'n_transactions': transactions.count(),
            })
            
    form = AddTransactionAccountForm(user, t_type, account_id)
    edit_form = EditAccountForm(user, account)
    return render(request, 'core/account.html', context={
        't_types': t_types,
        'opt_by_type': options_by_type,
        'form' : form,
        'account' : account,
        'transactions' : transactions,
        'edit_form' : edit_form,
        'n_transactions': transactions.count(),
    })
    
@login_required
def addAccount(request):
    user = request.user
    if request.method == 'POST':
        form = AddNewAccountForm(user, request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            balance = form.cleaned_data['balance']
            currency_id = form.cleaned_data['currency']
            description = form.cleaned_data['description']
            currency = Currency.objects.get(id=currency_id)
            
            account = Account.objects.create(
                user=user,
                name=name.capitalize(),
                balance=balance,
                currency=currency,
                description=description
            )
            
            return HttpResponseRedirect(reverse('core_accounts'))
            
        else:
            return render(request, 'core/add_account.html', context={
                'form': form,
            })
        
    form = AddNewAccountForm(user)
    return render(request, 'core/add_account.html', context={
        'form': form,
    })
    
@login_required
def editAccount(request, account_id):
    user = request.user
    account = user.accounts.get(id=account_id)
    if request.method == 'POST':
        pass
        # form = EditAccountForm(user, account, request.POST)
        # if form.is_valid():
        #     new_name = form.cleaned_data['name']
        #     new_type = form.cleaned_data['category_type']
            
        #     category.name = new_name
        #     category.category_type = new_type
            
        #     category.save()

        # else:
            # return HttpResponseRedirect(reverse('core_account', args=(account_id,)))
    return HttpResponseRedirect(reverse('core_account', args=(account_id,)))

@login_required
def deleteAccount(request, account_id):
    user = request.user
    account = user.accounts.get(id=account_id)
    if request.method == 'POST':
        pass
    return HttpResponseRedirect(reverse('core_account', args=(account_id,)))
    
