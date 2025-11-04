from django.shortcuts import render, get_object_or_404, HttpResponse
from store.models import Product
from category.models import Category
from carts.models import Cart, CartItem
from carts.views import __cart_id
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
        in_cart = CartItem.objects.filter(
            cart__cart_id=__cart_id(request), product=product).exists()
    except Exception as e:
        raise e
    context = {
        'product': product,
        'is_in_cart': in_cart
    }
    return render(request, 'store/product_detail.html', context)
