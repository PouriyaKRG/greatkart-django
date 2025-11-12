from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from store.models import Product, ReviewRating, ProductGallery
from category.models import Category
from carts.models import Cart, CartItem
from .forms import ReviewForms
from django.contrib import messages
from carts.views import __cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
import datetime
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from orders.models import OrderProduct

def store(request):
    products_count = 0
    products = Product.objects.all().filter(
        is_available=True).order_by('product_name')
    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    products_count = products.count()
    context = {
        'products': paged_products,
        'products_count': products_count,
    }
    return render(request, 'store/store_page.html', context)



def filter_category(request, category_slug=None):
    found_category = None
    products = None
    products_count = 0
    found_category = get_object_or_404(Category, slug=category_slug)

    products = Product.objects.all().filter(
        category=found_category).order_by('product_name')
    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    products_count = products.count()

    context = {
        'products': paged_products,
        'products_count': products_count
    }

    return render(request, 'store/store_page.html', context)






def product_detail(request, category_slug, product_slug):
    orderproduct = None
    if request.user.is_authenticated:
        try:
            product = Product.objects.get(
                    category__slug=category_slug, slug=product_slug)
            in_cart = CartItem.objects.filter(
                    cart__cart_id=__cart_id(request), product=product).exists()
        except Exception as e:
                raise e
            
        try:
                orderproduct = OrderProduct.objects.filter(user=request.user, product_id=product.id).exists()
                
        except (OrderProduct.DoesNotExist):
                orderproduct = None
                
        reviews = None
        review_exist = False    
        try:
                
                review_exist = ReviewRating.objects.filter(product_id = product.id).exists()
                
                if review_exist:
                    reviews = ReviewRating.objects.all().filter(product_id = product.id , status=True)

        except:        
                reviews = None
            
        product_gallery = ProductGallery.objects.filter(product_id= product.id)        
        context = {
                'product': product,
                'is_in_cart': in_cart,
                'is_product_ordered' : orderproduct,
                'reviewExist': review_exist,
                'reviews': reviews,
                'product_gallery':product_gallery
        
            }
        return render(request, 'store/product_detail.html', context)

    else:
        try:
            product = Product.objects.get(
                    category__slug=category_slug, slug=product_slug)
            in_cart = CartItem.objects.filter(
                    cart__cart_id=__cart_id(request), product=product).exists()
        except Exception as e:
                raise e
        reviews = None
        review_exist = False    
        try:
                
                review_exist = ReviewRating.objects.filter(product_id = product.id).exists()
                
                if review_exist:
                    reviews = ReviewRating.objects.all().filter(product_id = product.id , status=True)

        except:        
                reviews = None
        
        product_gallery = ProductGallery.objects.filter(product_id= product.id)                    
        context = {
                'product': product,
                'is_in_cart': in_cart,
                'is_product_ordered' : orderproduct,
                'reviewExist': review_exist,
                'reviews': reviews,
                'product_gallery': product_gallery
        
            }
        return render(request, 'store/product_detail.html', context)



def search(request):
    products_count = 0
   
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if  keyword:     
            products = Product.objects.order_by(
                '-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            products_count = products.count()

    context = {
        'products': products,
        'products_count': products_count
    }
    
    return render(request, 'store/store_page.html', context)




@login_required(login_url='login')
def submit_review(request,product_id):
    current_url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        try:
            reviews = ReviewRating.objects.get(user_id=request.user.id, product__id=product_id)
            form = ReviewForms(request.POST, instance=reviews)
            form.save()
            messages.success(request,'Thank you! Your Review has Been Updated')
            return redirect(current_url)
        except (IntegrityError, ReviewRating.DoesNotExist) as e:
            form = ReviewForms(request.POST)
            if form.is_valid():
                print('form is valid ')
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.review = form.cleaned_data['review']
                data.rating = form.cleaned_data['rating']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request,'Thank you! Your review has been submitted')
                return redirect(current_url)
    return redirect(current_url)        