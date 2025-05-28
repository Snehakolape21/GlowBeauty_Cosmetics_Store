from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class product(models.Model):
        name = models.CharField(max_length=100)  
        price = models.IntegerField()
        description = models.TextField()
        type=models.CharField(max_length=20,default='')
        image = models.ImageField(upload_to='images/')    
    
    
class Order(models.Model): 
    orderid=models.CharField(max_length=50,default='')
    userid = models.ForeignKey(User, on_delete=models.CASCADE,default='')
    productid = models.ForeignKey(product, on_delete=models.CASCADE) 
    quantity = models.IntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default='Pending')

    
    

class Cart(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE,default='')
    productid = models.ForeignKey(product, on_delete=models.CASCADE,default='')
    quantity = models.IntegerField(default=1)
      
    
