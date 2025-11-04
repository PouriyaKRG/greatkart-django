from django.urls import path
from carts import views
urlpatterns = [
    path('', views.cart_page, name='cart-page'),
    path('add_to_cart/<int:product_id>/', views.add_cart, name='add-to-cart'),
    path('suntract-from-cart/<int:product_id>/',
         views.subtract_cart, name="subtract-cart"),
    path('delete/<int:cartitem_id>/',
         views.remove_item, name="delete-cart-item"),
]
