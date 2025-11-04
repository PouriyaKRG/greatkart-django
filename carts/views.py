from django.shortcuts import render, redirect, get_object_or_404
from store import models as store_models
from carts import models as carts_models


def __cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def cart_page(request, totalPay=0, quantity=0, cart_items=None):
    grand_totalPay = 0.0
    tax = 0.0
    try:
        cart = carts_models.Cart.objects.get(cart_id=__cart_id(request))
        cart_items = carts_models.CartItem.objects.filter(
            cart=cart, is_active=True)
        for cart_item in cart_items:
            totalPay += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = 0.2 * totalPay
        grand_totalPay = totalPay + tax
    except:
        pass

    context = {
        'totalPay': totalPay,
        'qunatity': quantity,
        'cart_items': cart_items,
        'grand_totalPay': round(grand_totalPay, 2),
        'taxPay': round(tax, 2)
    }

    return render(request, 'store/cart.html', context=context)


def add_cart(request, product_id):
    product = store_models.Product.objects.get(id=product_id)
    cart = None
    try:
        cart = carts_models.Cart.objects.get(cart_id=__cart_id(request))
    except carts_models.Cart.DoesNotExist as e:
        cart = carts_models.Cart.objects.create(
            cart_id=__cart_id(request)
        )
    cart.save()

    try:
        cart_item = carts_models.CartItem.objects.get(
            product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except carts_models.CartItem.DoesNotExist as e:
        cart_item = carts_models.CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        cart_item.save()

    return redirect('cart-page')


def subtract_cart(request, product_id):
    cart = carts_models.Cart.objects.get(cart_id=__cart_id(request))
    product = get_object_or_404(store_models.Product, id=product_id)
    cart_item = carts_models.CartItem.objects.get(
        product=product, cart=cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart-page')


def remove_item(request, cartitem_id):
    cart = carts_models.Cart.objects.get(cart_id=__cart_id(request))
    cart_item = get_object_or_404(
        carts_models.CartItem, id=cartitem_id, cart=cart)
    cart_item.delete()
    return redirect('cart-page')
