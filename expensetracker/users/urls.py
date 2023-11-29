from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.userLogin, name='users_userLogin'),
    path('signup/', views.userSignUp, name='users_userSignUp'),
    path('signout/', views.userSignOut, name='users_userSignOut'),
]
