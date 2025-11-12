from django.urls import path
from .views import register, login, logout, activate, dashboard, forget_password,resetPassword_validate, reset_password,my_orders,edit_profile, change_password, order_details
urlpatterns = [
    path("", dashboard, name="home"),
    path('register/', register,     name='register'),
    path('login/',    login,        name='login'),
    path('logout/',    logout,      name='logout'),
    path('dashboard/',    dashboard,      name='dashboard'),
    path('activate/<uidb64>/<token>/',activate ,name='activate'),
    path('reset_password_confirmation/<uidb64>/<token>/',resetPassword_validate ,name='reset_password_validate'),
    path('forgetPassword/', forget_password, name='forgetPassword'),
    path('reset_password/', reset_password, name='reset-password'),
    path('myorders/',my_orders,name='my-orders'),
    path('editprofile/',edit_profile,name='edit-profile'),
    path('change_password/',change_password,name='change-password'),
    path('myorders/order_details/<str:order_number>', order_details, name='order-details'),
]
