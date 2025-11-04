from .models import CartItem, Cart
from carts.views import __cart_id


def count_cart_item(request):
    counter = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart_items = CartItem.objects.filter(
                cart__cart_id=__cart_id(request))
            for item in cart_items:
                counter += item.quantity
        except:
            return dict(count_items=counter)

    return dict(count_items=counter)
