from django.urls import path
from greatKart import views

urlpatterns = [
    path('', views.home_page, name='home-page')
]
