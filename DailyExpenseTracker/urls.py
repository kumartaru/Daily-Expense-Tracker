"""DailyExpenseTracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from expense.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Index,name='index'),
    path('register',register,name='register'),
    path('dashboard',dashboard,name='dashboard'),
    path('add_expense',add_expense,name='add_expense'),
    path('manage_expense',manage_expense,name='manage_expense'),
    path('delete_expense/<int:pid>',delete_expense,name='delete_expense'),
    path('expense_datewise',expense_datewise,name='expense_datewise'),
    path('expense_datewisedetail',expense_datewisedetail,name='expense_datewisedetail'),
    path('changepassword', changepassword, name='changepassword'),
    path('logout',Logout,name='logout'),
path('userprofile',userprofile,name='userprofile'),
]
