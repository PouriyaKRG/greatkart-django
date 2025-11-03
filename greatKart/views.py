from django.shortcuts import render, HttpResponse
from store.models import Product
from category.models import Category
# Create your views here.


def home_page(request):
    products = Product.objects.all().filter(is_available=True)
    context = {
        'products': products
    }
    return render(request, 'greatKart/home.html', context=context)
