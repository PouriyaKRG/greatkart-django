from django.shortcuts import render, HttpResponse
from store.models import Product, ReviewRating
from category.models import Category
# Create your views here.


def home_page(request):
    products = Product.objects.all().filter(is_available=True).order_by('created_date')
    
    for product in products:
        reviews = ReviewRating.objects.all().filter(product_id = product.id , status=True)

    context = {
        'products': products,
        'reviews': reviews,
    }
    return render(request, 'greatKart/home_page.html', context=context)
