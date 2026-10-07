from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView
from . import forms

urlpatterns = [
    path('', views.hello),
    path('login' , LoginView.as_view(authentication_form = forms.UserLoginForm) , name = 'login'),
    path('register', views.UserCreateView.as_view(), name='register'),
    path('' , include('django.contrib.auth.urls')),
]
