from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from store import models as store_models
from carts import models as carts_models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

def __cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def cart_page(request, totalPay=0, quantity=0, cart_items=None):
    try:
        grand_totalPay = 0.0
        tax = 0.0
        if request.user.is_authenticated:
            cart_items = carts_models.CartItem.objects.filter(user = request.user, is_active = True)
        else:    
            cart = carts_models.Cart.objects.get(cart_id=__cart_id(request))
            cart_items = carts_models.CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            totalPay += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = 0.2 * totalPay
        grand_totalPay = totalPay + tax
    except ObjectDoesNotExist:
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
    current_user = request.user
    if current_user.is_authenticated:
            product = store_models.Product.objects.get(id=product_id)
            product_variation = []
            if request.method == 'POST':
                for item in request.POST:
                    key = item
                    value = request.POST[key]

                    try:
                        variation = store_models.Variation.objects.get(product__id=product_id, variation_category__iexact=key, variation_value__iexact=value)
                        product_variation.append(variation)
                    except:
                        pass
            print(product_variation)            
            is_cart_item_exist = carts_models.CartItem.objects.filter(product=product, user=current_user).exists()
            if is_cart_item_exist:
                cart_items = carts_models.CartItem.objects.all().filter(product=product, user=current_user)
                
                ex_var_list = []
                id_list = []
                for item in cart_items:
                    existing_variation = item.variation.all()
                    ex_var_list.append([existing_variation[1],existing_variation[0]])
                    id_list.append(item.id)
                
                if product_variation in ex_var_list:
                    index = ex_var_list.index(product_variation)
                    item_id = id_list[index]
                    item = carts_models.CartItem.objects.get(
                        product=product, id=item_id)
                    item.quantity += 1
                    item.save()
                       
                else:
                    item = carts_models.CartItem.objects.create(
                        product=product, quantity=1, user=current_user)
                    if len(product_variation) > 0:
                        item.variation.clear()
                        item.variation.add(*product_variation)
                        item.quantity = 1
                    item.save()
            else:
                cart_item = carts_models.CartItem.objects.create(
                    product=product,
                    quantity=1,
                    user=current_user
                  
                )
                cart_item.save()
                if len(product_variation) > 0:
                    cart_item.variation.clear()
                    cart_item.variation.add(*product_variation)
 
            return redirect('cart-page')
    else:
        product = store_models.Product.objects.get(id=product_id)
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = store_models.Variation.objects.get(product__id=product_id,
                                                                variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        product = store_models.Product.objects.get(id=product_id)
        cart = None

        try:
            cart = carts_models.Cart.objects.get(cart_id=__cart_id(request))
        except carts_models.Cart.DoesNotExist as e:
            cart = carts_models.Cart.objects.create(cart_id=__cart_id(request))
        cart.save()

        is_cart_item_exist = carts_models.CartItem.objects.filter(
            product=product, cart=cart).exists()

        if is_cart_item_exist:
            cart_items = carts_models.CartItem.objects.filter(
                product=product, cart=cart)
            
            
            
            ex_var_list = []
            id_list = []
            for item in cart_items:
                existing_variation = item.variation.all()
                ex_var_list.append(list(existing_variation))
                id_list.append(item.id)





            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = id_list[index]
                item = carts_models.CartItem.objects.get(
                    product=product, id=item_id)
                item.quantity += 1
                item.save()
                
                
            else:
                item = carts_models.CartItem.objects.create(
                    product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variation.clear()
                    item.variation.add(*product_variation)
                    item.quantity = 1
                item.save()
        else:
            cart_item = carts_models.CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart
            )
            cart_item.save()
            if len(product_variation) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)

        return redirect('cart-page')


def subtract_cart(request, product_id, cart_item_id):
    current_user = request.user
    if current_user.is_authenticated:
        product = get_object_or_404(store_models.Product, id=product_id)
        try:
            cart_item = carts_models.CartItem.objects.get(product=product, user=current_user, id=cart_item_id)

            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()

        except:
            pass
    else:    
        cart = carts_models.Cart.objects.get(cart_id=__cart_id(request))
        product = get_object_or_404(store_models.Product, id=product_id)
        try:
            cart_item = carts_models.CartItem.objects.get(
                product=product, cart=cart, id=cart_item_id)

            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()

        except:
            pass

    return redirect('cart-page')



def remove_item(request, product_id, cart_item_id):
    current_user = request.user
    if current_user.is_authenticated:
        try:

            product = get_object_or_404(store_models.Product, id=product_id)
            cart_item = carts_models.CartItem.objects.get(product=product, user=current_user, id = cart_item_id)
            cart_item.delete()
        except:
            print('Throw except in delete')
            pass
    else:
        try:
            cart = carts_models.Cart.objects.get(cart_id=__cart_id(request))
            product = get_object_or_404(store_models.Product, id=product_id)
            cart_item = carts_models.CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
            cart_item.delete()
        except:
            pass    
    return redirect('cart-page')




@login_required(login_url='login')
def check_out(request, total=0,quantity=0, cart_items=None):
    grand_totalPay = 0.0
    tax = 0.0
    try:
        if request.user.is_authenticated:
            cart_items = carts_models.CartItem.objects.filter(user = request.user, is_active = True)
        else:    
            cart = carts_models.Cart.objects.get(cart_id=__cart_id(request))
            cart_items = carts_models.CartItem.objects.filter(cart=cart, is_active=True)
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
        tax = 0.2 * total
        grand_totalPay = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'totalPay': total,
        'qunatity': quantity,
        'cart_items': cart_items,
        'grand_totalPay': round(grand_totalPay, 2),
        'taxPay': round(tax, 2)
    }
    
    return render(request, 'store/checkout.html', context)