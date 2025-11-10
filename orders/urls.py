from django.urls import path
from . import views
urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('payment/', views.payment, name='payment'),
    path('payment-success/', views.paymentSuccessful, name='payment-sucess'),
    path('payment-failed/', views.paymentFailed, name='payment-failed'),
    path('payment-cancel/', views.paymentCancel, name='payment-cancel'),
    path('pay-product', views.create_checkout_session, name="create-checkout-session"),
    path('retry-payment/', views.retry_payment, name='retry_payment')
]