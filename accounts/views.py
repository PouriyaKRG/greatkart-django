from django.shortcuts import render,redirect, HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
#Verification if email
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


def logout_required(function=None, logout_url=settings.LOGOUT_URL):
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated,
        login_url=logout_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


@logout_required(logout_url='dashboard')
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name   = form.cleaned_data['first_name']
            last_name    = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email        = form.cleaned_data['email_address']
            password     = form.cleaned_data['password']
            username     = email.split('@')[0]
            user = Account.objects.create_user(
                first_name   = first_name,
                last_name    = last_name,
                phone_number = phone_number,
                email_address        = email,
                password     = password,
                user_name     = username
            )
            user.save()
            
            #USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Please verify your email address'
            message = render_to_string('accounts/account_verification_email.html',{
                'user':user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            
            messages.success(request, 'Thank you for registration, please go ahead and verify your account by verification email that we\'ve send to your email')
            redirect_to_email = f'/account/login/?command=verification&email={email}'
            
            return HttpResponseRedirect(redirect_to_email)
    else:
        form = RegistrationForm()
    context = {
        'form':form
    }
    return render(request, 'accounts/register_page.html',context)



@logout_required(logout_url='dashboard')
def login(request):
    if request.method == 'POST':
        email = request.POST['email_address']
        password = request.POST['password']
        user = auth.authenticate(email_address=email, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Login credentials')
            return redirect('login')

    return render(request, 'accounts/login_page.html')




@logout_required
def activate(request, uidb64, token):
    try:
       uid = urlsafe_base64_decode(uidb64).decode()
       user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
       user = None
  
    if user is not None and default_token_generator.check_token(user, token):
       user.is_active = True
       user.save()
       messages.success(request, 'Congratulation your accounts is activated') 
       return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        redirect('register')              
        
    return redirect('login')



@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request,'You have successfully logged out')
    return redirect('login')



@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')




def forget_password(request):
    if request.method == 'POST':
        email = request.POST['email_address']
        if Account.objects.filter(email_address=email).exists():
            user = Account.objects.get(email_address__iexact=email)
            
            # Change Password
            current_site = get_current_site(request)
            mail_subject = 'Reset Password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            
            messages.success(request,'Password reset email has been send to your email address.')
            return redirect('login')
        
        else:
            messages.error(request,'Sorry, we couldn\'t find the account for this email')
            return redirect('forgetPassword')
            
    return render(request, 'accounts/forgetPassword.html')



def resetPassword_validate(request ,uidb64, token):
    
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist) :
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('reset-password')
    else:
        messages.error(request,'This link has been expired')
        return redirect('login')
    
    
    
def reset_password(request):
    
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password changed successfully')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match')
            return redirect('reset-password')
    
    return render(request, 'accounts/reset_pass_page.html')    