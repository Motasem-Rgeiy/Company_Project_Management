from django.urls import path
from . import views

urlpatterns = [
   path('', views.RequestListView.as_view(), name='approval_list'),
   path('employee/reject/<int:pk>', views.request_reject, name='reject_view'),
   path('employee/accept/<int:pk>', views.request_accept, name='accept_view'),

]
