from django.urls import path
from cosmeticapp import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin



urlpatterns = [ 
    path('',views.index),
    path('register',views.register), 
    path('login',views.userlogin), 
    path('logout',views.userlogout),
    path('aboutus',views.aboutus),
    path('contactus',views.contactus),
    path('filter-by-cat/<productname>',views.filterByCategory),
    path('addtocart/<productid>',views.addtocart), 
    path('showmycart',views.showMyCart) , 
    path('removecart/<cartid>',views.removecart),  
    path('updatequantity/<cartid>/<operation>',views.updateQuantity) ,
    path('confirmorder',views.confirmorder),
    path('makepayment',views.makepayment),
    path('placeorder',views.placeorder),
    path('order_success',views.order_success),
    path('myorder',views.my_orders)
    



 
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   