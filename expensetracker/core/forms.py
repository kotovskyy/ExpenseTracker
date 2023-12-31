from django import forms
from datetime import date
from .models import Account, Currency, Icon, Color

class AddTransactionForm(forms.Form):
    INCOME = "I"
    EXPENSE = "E"
    TRANSFER = "T"
    TRANSACTION_TYPE_CHOICES = [
        (EXPENSE, "Expense"),
        (INCOME, "Income"),
        # (TRANSFER, "Transfer")
    ]
    transaction_type = forms.ChoiceField(
        choices=TRANSACTION_TYPE_CHOICES,
        initial=EXPENSE,
        required=False,
        widget=forms.Select(attrs={'class': 'form-field', 'id': 'transaction_type'})
    )
    category = forms.ChoiceField(
        choices=[],
        required=False,
        widget=forms.Select(attrs={'class': 'form-field', 'id': 'whereto_selector'})
    )
    amount = forms.DecimalField(
        label="Transaction Amount",
        max_digits=22,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-field amount-field'})
    )
    currency = forms.ChoiceField(
        choices=[(c.id, c.code) for c in Currency.objects.all()],
        initial=None,
        widget=forms.Select(attrs={'class': 'form-field currency-field'})
    )
    account = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-field'}),
        required=False
    )
    date = forms.DateField(
        label="Date",
        initial=date.today(),
        widget=forms.DateInput(
            attrs={'type': 'date',
                   'max' : date.today(),
                   'class': 'form-field'}
        )
    )
    description = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-field'})
    )
    

class AddTransactionCategoryForm(AddTransactionForm):
    def __init__(self, user, t_type, category_id=None, *args, **kwargs):
        super(AddTransactionCategoryForm, self).__init__(*args, **kwargs)
        self.fields['transaction_type'].initial = t_type
        self.fields['category'].initial = category_id
        self.fields['account'].choices = \
                [(acc.id, acc.name) for acc in user.accounts.all().order_by('id')]
        self.fields['currency'].initial = user.settings.first().main_currency
        if t_type == "I":
            self.fields['category'].choices = \
                [(c.id, c.name) for c in user.categories.filter(category_type="I").order_by('id')]
        else:
            self.fields['category'].choices = \
                [(c.id, c.name) for c in user.categories.filter(category_type="E").order_by('id')]

class AddTransactionAccountForm(AddTransactionForm):
    def __init__(self, user, t_type, account_id=None, *args, **kwargs):
        super(AddTransactionAccountForm, self).__init__(*args, **kwargs)
        account = Account.objects.get(id=account_id)
        self.fields['account'].initial = account_id
        self.fields['currency'].initial = account.currency.id
        self.fields['category'].choices = \
                [(c.id, c.name) for c in user.categories.all().order_by('id')]
        

class EditAccountForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        initial=None,
        widget=forms.TextInput(attrs={'class': 'form-field'})
    )
    balance = forms.DecimalField(
        max_digits=22,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-field amount-field amount-currency-shared'})
    )
    currency = forms.ChoiceField(
        choices=[(c.id, c.code) for c in Currency.objects.all()],
        widget=forms.Select(attrs={'class': 'form-field currency-field'})
    )
    description = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-field'})
    )
    
    def __init__(self, user, account, *args, **kwargs):
        super(EditAccountForm, self).__init__(*args, **kwargs)
        self.fields['name'].initial = account.name
        self.fields['currency'].initial = account.currency.id
        self.fields['balance'].initial = account.balance
        self.fields['description'].initial = account.description


class EditCategoryForm(forms.Form):
    INCOME = "I"
    EXPENSE = "E"
    CATEGORY_TYPE_CHOICES = (
        (INCOME, "Income"),
        (EXPENSE, "Expense")
    )
    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
        'autocomplete': 'off',
        'class' : 'form-field'
        })
    )
    category_type = forms.ChoiceField(
        choices=CATEGORY_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-field'})
    )
    
    def __init__(self, user, category, *args, **kwargs):
        super(EditCategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].initial = category.name
        self.fields['category_type'].initial = category.category_type


class EditTransactionForm(AddTransactionForm):
    def __init__(self, user, transaction, *args, **kwargs):
        super(EditTransactionForm, self).__init__(*args, **kwargs)
        self.fields['account'].choices = \
                [(acc.id, acc.name) for acc in user.accounts.all().order_by('id')]
        
        if transaction.transaction_type == "E":
            self.fields['category'].choices = \
                [(c.id, c.name) for c in user.categories.filter(category_type="E").order_by('id')]
        else:
            self.fields['category'].choices = \
                [(c.id, c.name) for c in user.categories.filter(category_type="I").order_by('id')]
            
        self.fields['transaction_type'].initial = transaction.transaction_type
        self.fields['amount'].initial = transaction.amount
        self.fields['currency'].initial = transaction.currency.id
        self.fields['category'].initial = transaction.category.id
        self.fields['account'].initial = transaction.account.id
        self.fields['description'].initial = transaction.description
        self.fields['date'].initial = transaction.date


class AddNewAccountForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        initial=None,
        widget=forms.TextInput(attrs={'class': 'form-field'})
    )
    balance = forms.DecimalField(
        max_digits=22,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-field amount-field amount-currency-shared'})
    )
    currency = forms.ChoiceField(
        choices=[(c.id, c.code) for c in Currency.objects.all()],
        widget=forms.Select(attrs={'class': 'form-field currency-field'})
    )
    description = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-field'})
    )
    
    def __init__(self, user, *args, **kwargs):
        super(AddNewAccountForm, self).__init__(*args, **kwargs)
        self.fields['currency'].initial = user.settings.first().main_currency.id

class AddNewCategoryForm(forms.Form):
    INCOME = "I"
    EXPENSE = "E"
    CATEGORY_TYPE_CHOICES = [
        (INCOME, "Income"),
        (EXPENSE, "Expense")
    ]
    name = forms.CharField(
        max_length=50,
        initial=None,
        widget=forms.TextInput(attrs={'class': 'form-field'})
    )
    category_type = forms.ChoiceField(
        choices=CATEGORY_TYPE_CHOICES,
        initial=EXPENSE,
        widget=forms.Select(attrs={'class': 'form-field'})
    )
    icon = forms.ChoiceField(
        choices=[(i.id, i.path) for i in Icon.objects.all()],
        widget=forms.Select(attrs={'class': 'form-field'}),
    )
    color = forms.ChoiceField(
        choices=[(c.id, c.hex_value.upper()) for c in Color.objects.all()],
        widget=forms.Select(attrs={'class': 'form-field'})
    )
    
    def __init__(self, def_type=None, *args, **kwargs):
        super(AddNewCategoryForm, self).__init__(*args, **kwargs)
        if def_type is not None:
            self.fields['category_type'].initial = def_type
      
        self.fields['color'].initial = Color.objects.get(hex_value="#bd83b8".casefold()).id
        self.fields['icon'].initial = Icon.objects.first()
        
class SettingsForm(forms.Form):
    main_currency = forms.ChoiceField(
        choices=[(c.id, c.code) for c in Currency.objects.all()],
        widget=forms.Select(attrs={'class': 'form-field'})
    )
    
    def __init__(self, user, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.fields['main_currency'].initial = user.settings.first().main_currency.id
