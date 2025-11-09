from django.urls import path
from carts import views
urlpatterns = [
    path('', views.cart_page, name='cart-page'),
    path('add_to_cart/<int:product_id>/', views.add_cart, name='add-to-cart'),
    path('suntract-from-cart/<int:product_id>/<int:cart_item_id>/', views.subtract_cart, name="subtract-cart"),
    path('delete/<int:product_id>/<int:cart_item_id>?', views.remove_item, name="delete-cart-item"),
    path('checkout/', views.check_out, name='checkout')
]
