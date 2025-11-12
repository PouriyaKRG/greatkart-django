from django import forms
from .models import Account, UserProfile
from django.contrib import messages



class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': ' Enter password',
        'class' : 'form-control'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': ' Confirm password',
        'class' : 'form-control'
    }))
    
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email_address', 'password']
    
    
    def __init__(self,*args,**kargs):
        super(RegistrationForm, self).__init__(*args,**kargs)
        self.fields['first_name'].widget.attrs['placeholder'] = "Enter name here"
        self.fields['last_name'].widget.attrs['placeholder'] = "Enter lastname here"
        self.fields['phone_number'].widget.attrs['placeholder'] = "Enter phone number here"
        self.fields['email_address'].widget.attrs['placeholder'] = "Enter email address here"
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'            
            
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')  
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError(
                'Password doesn\'t match!'
            ) 
   
   
   
   
class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name','last_name','phone_number')   
        
    def __init__(self,*args,**kargs):
        super(UserForm,self).__init__(*args,**kargs)    
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        
class UserProfileForm(forms.ModelForm):
    
    
    profile_picture = forms.ImageField(required=False, error_messages= {'invalid': ("Image files only")}, widget=forms.FileInput)
    
    class Meta:
        model = UserProfile
        fields = ('address_line_1','address_line_2','city','state','country','profile_picture')     
   
   
    def __init__(self,*args,**kargs):
        super(UserProfileForm,self).__init__(*args,**kargs)    
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'     