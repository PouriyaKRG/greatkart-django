from django.shortcuts import render,HttpResponse,redirect
from django.template.loader import render_to_string
from carts.models import CartItem
from orders.models import Order,OrderProduct,Payment
from .forms import OrderForm
import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
import stripe
from store.models import Product
stripe.api_key = settings.STRIPE_SECRET_KEY
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import stripe
from store.models import Product

# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def create_checkout_session(request):
        # Get the order from session
        order_id = request.session.get('order_id')
        if not order_id:
            messages.error(request, "No order found. Please place your order again.")
            return redirect('place_order')
        
        order = get_object_or_404(Order, id=order_id, user=request.user, is_ordered=False)
        
        YOUR_DOMAIN = f"{request.scheme}://{request.get_host()}"
        
        # Method 1: Single line item with order total (Simplest)
        line_items = [{
            'price_data': {
                'currency': 'usd',
                'unit_amount': int(order.orderTotal * 100),  # Total including tax
                'product_data': {
                    'name': f'Order #{order.order_number}',
                    'description': f'Total amount including ${order.tax} tax',
                },
            },
            'quantity': 1,
        }]
        
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            metadata={
                'order_id': order.id,
                'user_id': request.user.id,
                'order_number': order.order_number
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/orders/payment-success/',
            cancel_url=YOUR_DOMAIN + '/orders/payment-cancel/',
            customer_email=request.user.email_address,
        )
        
        return redirect(checkout_session.url)
        

@login_required
def paymentSuccessful(request):
    try:
        order_id = request.session.get('order_id')
        if not order_id:
            messages.error(request, "No order found. Please check your order history.")
            return redirect('store-page')
        
        order = get_object_or_404(Order, id=order_id, user=request.user)
        
        if order.is_ordered:
            messages.info(request, "This order has already been processed.")
            sub_total = 0    
            order_products = OrderProduct.objects.all().filter(order=order)
            for product in order_products:
                sub_total += (product.quantity * product.product_price)
            context = {
                'order': order,
                'ordered_products':  order_products,
                'subTotal' : sub_total
                }
            return render(request, 'orders/payment_success.html', context)
        
        payment = Payment(
            user=request.user,
            payment_id=f"stripe_{order_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            payment_method='Stripe',
            amount_paid=str(order.orderTotal),
            status='Completed'
        )
        payment.save()
        
        order.payment = payment
        order.is_ordered = True
        order.status = 'Completed'
        order.save()
        
        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            # Get the first variation if exists, or None
            
            order_product = OrderProduct(
                order=order,
                payment=payment,
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                product_price=item.product.price,
                ordered=True
            )
            order_product.save()
            
            cart_item = CartItem.objects.get(id=item.id)
            product_variations = cart_item.variation.all()
            orderProduct = OrderProduct.objects.get(id=order_product.id)
            orderProduct.variation.set(product_variations)
            orderProduct.save()
            
            
            
            product = Product.objects.get(id=item.product_id)
            product.stock -= item.quantity 
            product.save()   
            
            if product.stock < 1 :
                messages.warning('Product Quantity is not enough')
            
        sub_total = 0    
        order_products = OrderProduct.objects.all().filter(order=order)
        for product in order_products:
            sub_total += (product.quantity * product.product_price)
    
        cart_items.delete()
        
        if 'order_id' in request.session:
            del request.session['order_id']
        
        context = {
            'order': order,
            'ordered_products': order_products,
            'subTotal': sub_total
        }
        
        mail_subject = 'GreatKart , Thank You For Your Order'
        message = render_to_string('orders/order_recieved_email.html',{
                'user':  request.user,
                'order': order,               
            })
        to_email = request.user.email_address
        send_email = EmailMessage(mail_subject, message, to=[to_email, order.email])
        send_email.send()
        
        return render(request, 'orders/payment_success.html', context)
        
    except Exception as e:
        print(f"Error in payment success: {str(e)}")
        messages.error(request, "Error processing your payment. Please contact support.")
        return redirect('payment-failed')
        
@login_required
def paymentCancel(request):
    return render(request, 'orders/payment_cancel.html')


@login_required
def paymentFailed(request):
    """Handle all types of payment failures"""
    try:
        # Get the order from session
        order_id = request.session.get('order_id')
        order = None
        
        if order_id:
            try:
                order = Order.objects.get(id=order_id, user=request.user, is_ordered=False)
            except Order.DoesNotExist:
                order = None
                # Clear invalid order from session
                if 'order_id' in request.session:
                    del request.session['order_id']
        
        # Get any error messages passed from previous views
        storage = messages.get_messages(request)
        error_messages = []
        for message in storage:
            error_messages.append(message.message)
        
        # If no specific error message, use appropriate generic ones
        if not error_messages:
            if order:
                error_messages = ["Payment processing failed. Please try again."]
            else:
                error_messages = ["Unable to process payment. Please place a new order."]
        
        # Get cart items count for context
        cart_items_count = 0
        if request.user.is_authenticated:
            cart_items_count = CartItem.objects.filter(user=request.user).count()
        
        context = {
            'order': order,
            'error_messages': error_messages,
            'order_id': order_id,
            'cart_items_count': cart_items_count,
        }
        return render(request, 'orders/payment_failed.html', context)
        
    except Exception as e:
        print(f"Error in payment_failed view: {str(e)}")
        # Fallback context in case of any errors
        context = {
            'order': None,
            'error_messages': ["An unexpected error occurred. Please try again."],
            'cart_items_count': 0,
        }
        return render(request, 'orders/payment_failed.html', context)

@login_required
def retry_payment(request):
    """Allow users to retry payment for the same order"""
    try:
        order_id = request.session.get('order_id')
        if not order_id:
            messages.error(request, "No order found. Please place a new order.")
            return redirect('place_order')
        
        order = Order.objects.get(id=order_id, user=request.user, is_ordered=False)
        
        # Log retry attempt
        print(f"Payment retry attempted for order: {order.order_number}")
        
        return redirect('create_checkout_session')
        
    except Order.DoesNotExist:
        messages.error(request, "Order not found or already completed. Please place a new order.")
        return redirect('place_order')
    except Exception as e:
        print(f"Error in retry_payment: {str(e)}")
        messages.error(request, "Unable to retry payment. Please try placing a new order.")
        return redirect('payment-failed')


@login_required
def payment(request):
    return render(request, 'orders/payments.html')



@login_required
def place_order(request, total = 0,quantity = 0, cart_items = None):
    current_user = request.user

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    
    if cart_count <= 0 :
        return redirect('store-page')

    grand_total = 0.0
    tax = 0.0
    for item in cart_items:
        total += (item.product.price * item.quantity)
        quantity += item.quantity
    tax = (20*total) / 100
    grand_total = total  + tax  
    if request.method == 'POST':
        form = OrderForm(request.POST)  
  
        if form.is_valid():
           data = Order()
           data.user = current_user
           data.first_name = form.cleaned_data['first_name']
           data.last_name = form.cleaned_data['last_name']
           data.phone = form.cleaned_data['phone']
           data.email = form.cleaned_data['email']
           data.addressLine1 = form.cleaned_data['addressLine1']
           data.addressLine2 = form.cleaned_data['addressLine2']
           data.country = form.cleaned_data['country']
           data.state = form.cleaned_data['state']
           data.city = form.cleaned_data['city']
           data.orderNote = form.cleaned_data['orderNote']
           data.orderTotal = grand_total
           data.tax = tax
           data.ip = request.META.get('REMOTE_ADDR')
           data.save() 
           # Generate Order Number
           yr = int(datetime.date.today().strftime('%Y'))
           dt = int(datetime.date.today().strftime("%d"))
           mt = int(datetime.date.today().strftime('%m'))
           d = datetime.date(yr,mt,dt)
           current_date = d.strftime('%Y%m%d')
           order_number = 'gk-'+current_date + str(data.id) +str(data.user.id)
           data.order_number = order_number
           data.save()
           request.session['order_id'] = data.id
           order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
           context = {
               'order': order,
               'cart_items':cart_items,
               'total': round(total,2),
               'grand_total': round(grand_total,2),
               'tax': round(tax,2)
           }
        return render(request, 'orders/payments.html', context)
       
    else:
        return redirect('checkout')   