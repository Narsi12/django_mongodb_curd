from django.contrib import admin
from django.urls import path
from .views import create_employee,get_users,update_employee,delete_user
urlpatterns = [
    path('create',create_employee, name='create_employee'),
    path('get',get_users, name='get_users'),
    path('update/<str:pk>',update_employee, name='update_employee'),
    path('delete/<str:pk>',delete_user, name='delete_user'),
    
]
