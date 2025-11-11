from django.urls import path
from store import views


urlpatterns = [
    path('', views.store, name='store-page'),
    path('submitReview/<int:product_id>/', views.submit_review, name='submit-review'),
    path('search/', views.search, name='search'),
    path('filter/<slug:category_slug>/',views.filter_category, name='filter-category'),
    path('<slug:category_slug>/<slug:product_slug>/',views.product_detail, name='product-detail'),
]
