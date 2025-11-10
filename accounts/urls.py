from django.urls import path
from .views import register, login, logout, activate, dashboard, forget_password,resetPassword_validate, reset_password
urlpatterns = [
    path("", dashboard, name="home"),
    path('register/', register,     name='register'),
    path('login/',    login,        name='login'),
    path('logout/',    logout,      name='logout'),
    path('dashbaord/',    dashboard,      name='dashboard'),
    path('activate/<uidb64>/<token>/',activate ,name='activate'),
    path('reset_password_confirmation/<uidb64>/<token>/',resetPassword_validate ,name='reset_password_validate'),
    path('forgetPassword/', forget_password, name='forgetPassword'),
    path('reset_password/', reset_password, name='reset-password'),
]
