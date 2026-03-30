"""PredictionofHepatitisDisease URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from Spam_Detection_In_Short_Message_Service import views as mainView
from admins import views as admins
from users import views as usr

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path("", mainView.index, name="index"),
    path("start/index/", mainView.index, name="index"),
    path("start/logout/", mainView.logout, name="logout"),
    path("start/UnifiedLogin/", mainView.UnifiedLogin, name="UnifiedLogin"),
    path("start/LoginCheck/", mainView.LoginCheck, name="LoginCheck"),
    path("start/UserRegister/", mainView.UserRegister, name="UserRegister"),
#adminviews
    path("admin/AdminLoginCheck/", admins.AdminLoginCheck, name="AdminLoginCheck"),
    path("admin/AdminHome/", admins.AdminHome, name="AdminHome"),
    path('admin/RegisterUsersView/', admins.RegisterUsersView, name='RegisterUsersView'),
    path('admin/ActivaUsers/', admins.ActivaUsers, name='ActivaUsers'),
    path('admin/DeleteUser/', admins.DeleteUser, name='DeleteUser'),
    path('admin/EditUser/', admins.EditUser, name='EditUser'),
    path('admin/ViewActivityLog/', admins.ViewActivityLog, name='ViewActivityLog'),
    path('admin/ViewPredictionReport/', admins.ViewPredictionReport, name='ViewPredictionReport'),

#User Views

    path("user/UserRegisterActions/", usr.UserRegisterActions, name="UserRegisterActions"),
    path("user/UserLoginCheck/", usr.UserLoginCheck, name="UserLoginCheck"),
    path("user/UserHome/", usr.UserHome, name="UserHome"),
    path("user/DatasetView/", usr.DatasetView, name="DatasetView"),
    path("user/machine_learning/",usr.machine_learning,name="machine_learning"),
    path("user/prediction/", usr.prediction, name="prediction"),
    path("user/UserReportView/", usr.UserReportView, name="UserReportView"),
]
