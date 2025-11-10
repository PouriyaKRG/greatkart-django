from django.contrib import admin
from .models import Payment, Order, OrderProduct
# Register your models here.



class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    readonly_fields = ['variation','payment','user','product','quantity','product_price','order','ordered']



class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name','phone','email','orderTotal','status', 'is_ordered', 'createdAt' ,'ip']
    list_filter = ['status','is_ordered']
    readonly_fields = ['user','payment','order_number','orderTotal','tax','ip']
    search_fields = ['order_number','first_name','last_name','phone','email']
    list_per_page = 20
    inlines = [OrderProductInline]



admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)