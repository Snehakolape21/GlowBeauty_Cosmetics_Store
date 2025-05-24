from django.shortcuts import render
from cosmeticapp.models import product, Order, Cart
from django.contrib.auth.models import  User  
from django.contrib.auth import authenticate , login , logout
from django.shortcuts import redirect
import razorpay
import uuid
# from django.utils.crypto import get_random_string


 

# Create your views here.

from django.shortcuts import render,redirect
from .models import product

def index(request): #qury data using the object - relational mapping (orm)  
    products = product.objects.all() #retrive all object of model  
    return render(request, 'index.html', {'products': products}) #return html templates and return the http response 
# equest object passses to the view function  // render the templates with data and return user. 
#the dictory is context . it contain key-value paire in index tamppate we can access data in key 
# pass data from view to templates .  make data availabe for rending in the templates .   



def userlogin(request): 
        if request.method=="GET": 
            return render(request, 'login.html')    
        else:
            '''1.fetch data '''
            u=request.POST['username'] 
            p=request.POST['password'] #capture form data  
             
            user= authenticate(username=u ,password= p) #inbuilt authethticate tunnction  . it verify only if password and username same or not 
            # when user login it will create session . and authnthicate only verify username and pasword if coorect will get user object.
            # print("login user after authenticate",user) 
            if user is not None: #succesfully login 
                login(request,user)
                return redirect("/") 
            else:
                context={}
                context["error"]='plz enter valid credential'
                return render(request,'login.html',context) 
# authenticate() checks username & password.
# login() creates a session for the user.
# If failed, shows error message.  
            
def register(request):
    if request.method=="GET":   #render register page its load templates fom teplates django handle template rendering 
        return render(request,'register.html')     
    else:
        u=request.POST['username']   #form input  
        e=request.POST['email']
        p=request.POST['password'] 
        cp=request.POST['Confirmpassword']     
        
        context={}
        
        if u=="" or e=="" and e=="@gmail.com" or p=="" or cp=="" :  
            context['error']='all the field are compulsory' 
            return render(request,'register.html',context)     
        elif p != cp:
            context['error']='password and confirm password must be same.'    
            return render(request,'register.html',context)    
        else:
            # user= User.objects.create(username=u,email=e,password=p)   #model class name  (db column name)  
            user = User.objects.create(username=u,email=e)  #auth_user    
            user.set_password(p) #encrypted password      . protect user account 
            user.save()  
            
            return redirect('/login') 
        
def aboutus(request):
    return render(request,'about.html')

def contactus(request):
    return render(request,'contact.html')
        
def userlogout(request):
    logout(request) 
    return redirect("/")  

            
def addtocart(request,productid):
    selectedpetObject= product.objects.get(id=productid)  #petid  
    userid = request.user.id  #user id 
    if userid is not None: 
        
        loggedInUserObject = User.objects.get(id = userid)  #if user is login 
        cart = Cart.objects.create(uid=loggedInUserObject,productid=selectedpetObject) 
        cart.save()
        # messages.success(request,'pet added to cart successfully') 
        return redirect('/')   
    else: 
        
        return redirect('/login')   


def filterByCategory(request, productname):   
    products = product.objects.filter(type=productname)
    return render(request, 'index.html', {'products': products})

def showMyCart(request):
    userid = request.user.id 
    user=User.objects.get(id=userid) 
    myCart=Cart.objects.filter(uid=user)  
    context={'mycart':myCart} 
    count = len(myCart)
    totalbill =  0  
    for cart in myCart: 
        totalbill += cart.productid.price * cart.quantity   
    context['count'] = count 
    context['totalbill'] = totalbill   
    return render(request,'addtocart.html',context)  


def removecart(request,cartid):
    c= Cart.objects.filter(id=cartid)  
    c.delete()  
    return redirect('/showmycart')  

def updateQuantity(request,cartid,operation): 
    cart= Cart.objects.filter(id=cartid)  
    if operation=='incr':
        q= cart[0].quantity
        cart.update(quantity=q+1)
        return redirect('/showmycart')  
    else:
        q=cart[0].quantity
        cart.update(quantity=q-1)
        return redirect('/showmycart')
    

def confirmorder(request) :
    userid = request.user.id 
    user= User.objects.get(id=userid)
    mycart = Cart.objects.filter(uid=user)
    context={'mycart' :mycart}
    count =len(mycart)
    totalbill = 0
    for cart in mycart:
        totalbill += cart.productid.price * cart.quantity
    context['count'] = count
    context['totalbill'] = totalbill
    return render(request,'confirmorder.html',context)

def makepayment(request):
    userid = request.user.id 
    data = Cart.objects.filter(uid= userid) 
    total = 0
    for cart in data:
        total += cart.productid.price*cart.quantity   
    client = razorpay.Client(auth=("rzp_test_5tcqyKP7gK3N5l" , "7p6xDqY81DWrnHdYUntGeOmw"))  
    
    data = { "amount": total*100,"currency" :"INR" ,"receipt" :""}  
    payment = client.order.create(data=data)  
    # print(payment) 
    context={} 
    context['data'] = payment  

    return render(request,'pay.html',context)

def placeorder(request): 

    if not request.user.is_authenticated:
        return redirect('/login')

    user = request.user
    ordid = uuid.uuid4()
    cartlist = Cart.objects.filter(uid=user)

    if not cartlist:
        return redirect('/showmycart')

    total = 0
    for cart in cartlist:
        Order.objects.create(
            orderid=ordid,
            userid=user,
            productid=cart.productid,
            quantity=cart.quantity
        )
        total += cart.productid.price * cart.quantity

    cartlist.delete()

    client = razorpay.Client(auth=("rzp_test_5tcqyKP7gK3N5l", "7p6xDqY81DWrnHdYUntGeOmw"))
    payment = client.order.create(data={
        "amount": total * 100,  # in paise  
        "currency": "INR",
        "receipt": str(ordid)
    })

    return render(request, 'pay.html', {
        'total': total,
        'data': payment  
    }) 
  
 
def order_success(request):
    return render(request, 'order_success.html') 
 

from django.contrib.auth.decorators import login_required

@login_required
def my_orders(request):
    user = request.user
    orders = Order.objects.filter(userid=user).order_by('-id')  # latest first
    context = {
        'orders': orders
    }
    return render(request, 'myorder.html', context) 
