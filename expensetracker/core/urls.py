from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="core_index"),
    path('categories/', views.categories, name='core_categories'),
    path('accounts/', views.accounts, name='core_accounts'),
    path('transactions/', views.transactions, name='core_transactions'),
]
