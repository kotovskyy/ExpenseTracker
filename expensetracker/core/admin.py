from django.contrib import admin
from .models import (Currency,
                     Settings,
                     Account,
                     Category,
                     Transaction,
                     Icon)

# Register your models here.
admin.site.register([Currency, Settings, Account, Category, Transaction, Icon])
