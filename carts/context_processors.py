from .models import CartItem, Cart
from carts.views import __cart_id


def count_cart_item(request):
    counter = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id= __cart_id(request))
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user = request.user )
            else:
                cart_items = CartItem.objects.all().filter(cart=cart[:1])      
            for item in cart_items:
                counter += item.quantity
        except:
            return dict(count_items=counter)

    return dict(count_items=counter)
