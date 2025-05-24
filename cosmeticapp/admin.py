from django.contrib import admin
from cosmeticapp.models import product, Order, Cart
# Register your models here.

class ProductAdmin(admin.ModelAdmin): 
    list_display=['id', 'name', 'price', 'description', 'type','image']
    list_filter=['type']
    
class OrderAdmin(admin.ModelAdmin):
    list_display=['id','orderid', 'userid', 'productid', 'quantity', 'order_date']
    list_filter=['userid', 'productid'] 
    
class CartAdmin(admin.ModelAdmin):
    list_display=['id', 'uid', 'productid', 'quantity']

admin.site.register(product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, CartAdmin)  