from django.shortcuts import render, get_object_or_404
from store.models import Product
from category.models import Category
# Create your views here.


def store(request):
    products = Product.objects.all().filter()
    products_count = products.count()
    context = {
        'products': products,
        'products_count': products_count
    }
    return render(request, 'store/store_page.html', context)


def filter_category(request, category_slug=None):
    found_category = None
    products = None
    products_count = 0
    found_category = get_object_or_404(Category, slug=category_slug)

    products = Product.objects.all().filter(
        category=found_category)
    products_count = products.count()

    context = {
        'products': products,
        'products_count': products_count
    }

    return render(request, 'store/store_page.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get(
            category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e
    context = {
        'product': product
    }
    return render(request, 'store/product_detail.html', context)
