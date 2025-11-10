from django import forms
from .models import Account
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
   