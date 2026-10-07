from django.urls import path
from . import views

urlpatterns = [
    path('subscribe', views.subscribe_view, name='subscribe_email'),
    path('confirm-email/<str:token>/', views.email_confirm, name='email_confirm'),
    path('', views.newsletter_list, name='newsletter_list'),
    path('send', views.newsletter_operations, name='newsletter_send')
]
