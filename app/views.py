from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,Cart,Order
from .form import OrderForm,Registeration,LoginForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
import stripe
stripe.api_key=settings.STRIPE_SECRET_KEY
# Create your views here.

def home(request):
    a=Product.objects.all()
    return render(request,'app1/home.html',{'product':a})

def user_creation(request):
    a=Registeration(request.POST or None)
    if request.method=='POST' and a.is_valid():
        a.save()
        return redirect ('home')
    return render(request,'app1/regform.html',{'form':a})

def loginform(request):
    a=LoginForm(request, data=request.POST or None)
    if request.method=='POST' and a.is_valid():
         user=a.get_user()
         login(request,user)
         return redirect('home')
    return render(request,'app1/log.html',{'form':a})

def logout_view(request):
    logout(request)
    return redirect('log')

@login_required
def Addcart(request,id):
    a=Product.objects.get(id=id)
    cart_items,created=Cart.objects.get_or_create(product=a, user=request.user)
    if not created:
        cart_items.quantity+=1
        cart_items.save()
    return redirect('cart')

def view_cart(request):
    a=Cart.objects.filter(user=request.user)
    return render(request,'app1/cart.html',{'cart':a})

def product_details(request,id):
    a=Product.objects.get(id=id)
    return render(request,'app1/details.html',{'product':a}) 

def dlt(request,id):
    a=Cart.objects.get(id=id)
    if a.quantity>1:
        a.quantity-=1
        a.save()
    else:
        a.delete()
    return redirect('cart')  


def add(request,id):
    a=Cart.objects.get(id=id)
    if a.quantity>1:
        a.quantity+=1
        a.save()
    else:
        a.delete()
    return redirect('cart') 


def previous_orders(request):
    a=Order.objects.filter(user=request.user)
    return render(request,'app1/orders.html',{'orders':a})


def buy_now(request,id):
    cart_items=get_object_or_404(Cart,id=id, user=request.user)
    a=cart_items.product

    session=stripe.checkout.Session.create (
         payment_method_types=['card'],
         line_items=[
           {
              'price_data':{
                  'currency':'inr',
                  'product_data':{
                      'name':a.name,
                   },
                   'unit_amount':int(float(a.price)*100),
               },
               'quantity':cart_items.quantity,
               
           }   
        ],

        mode="payment",
        success_url=request.build_absolute_uri(reverse('success',args=[id])),
        cancel_url=request.build_absolute_uri(reverse('cancel')),
    )
    return redirect(session.url)

def success(request,id):

    cart=Cart.objects.filter(id=id,user=request.user).delete()
    return render(request,'app1/success.html')

def cancel(request):
    return render(request,'app1/cancel.html')
