from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="core_index"),
    path('categories/', views.categories, name='core_categories'),
    path('accounts/', views.accounts, name='core_accounts'),
    path('transactions/', views.transactions, name='core_transactions'),
    path('categories/<int:category_id>/', views.category, name='core_category'),
    path('categories/<int:category_id>/edit/', views.editCategory, name='core_editCategory'),
    path('categories/<int:category_id>/delete/', views.deleteCategory, name='core_deleteCategory'),
    path('categories/add/', views.addCategory, name='core_addCategory'),
    path('accounts/<int:account_id>/', views.account, name='core_account'),
    path('accounts/add/', views.addAccount, name='core_addAccount'),
]
