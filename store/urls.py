from django.urls import path
from store import views


urlpatterns = [
    path('', views.store, name='store-page'),
    path('filter/<slug:category_slug>/',
         views.filter_category, name='filter-category'),
    path('<slug:category_slug>/<slug:product_slug>/',
         views.product_detail, name='product-detail'),
    path('search/', views.search, name='search')
]
