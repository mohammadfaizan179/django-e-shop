from itertools import product
from unicodedata import category
from django.contrib.messages.constants import SUCCESS
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from .models import Product, Customer, Cart, Order_Place
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import DetailView
from .forms import UserRegistrationForm, UserProfileForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class HomeView(View):
    def get(self, request):
        totalItem = 0
        top_wears = Product.objects.filter(category='TW')
        bottom_wears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        if request.user.is_authenticated:
            totalItem = len(Cart.objects.filter(user=request.user))
        context = {
            'bottom_wears' : bottom_wears,
            'top_wears' : top_wears,
            'mobiles' : mobiles,
            'totalItem' : totalItem
        }
        return render(request, 'app/home.html', context)

class ProductDetailView(View):
    def get(self,request,pk):
        totalItem = 0
        product_in_cart = False
        if request.user.is_authenticated:
            product_in_cart = Cart.objects.filter(Q(product=pk), Q(user=request.user)).exists()
        product = Product.objects.get(pk=pk)
        if request.user.is_authenticated:
            totalItem = len(Cart.objects.filter(user=request.user))
        context = {
            'product':product,
            'product_in_cart': product_in_cart,
            'totalItem' : totalItem
        }
        return render(request, 'app/productdetail.html', context)

@login_required
def add_to_cart(request):
    totalItem = 0
    user = request.user
    prod_id = request.GET.get('prod_id')
    product = Product.objects.get(id=prod_id)
    Cart(user=user, product=product).save()
    if request.user.is_authenticated:
            totalItem = len(Cart.objects.filter(user=request.user))
    context = {
        "totalItem" : totalItem
    }
    return redirect('/cart')

@login_required
def show_cart(request):
    totalItem = 0
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_products = [ p for p in Cart.objects.all() if p.user == user]
        if cart_products:
            for cart_product in cart_products:
                amount = amount + (cart_product.product.discount_price*cart_product.quantity)
            total_amount = amount + shipping_amount
            totalItem = len(Cart.objects.filter(user=request.user))
            return render(request, 'app/addtocart.html', {'carts':cart,'amount':amount,'total_amount':total_amount, 'totalItem':totalItem})
        else:
            totalItem = len(Cart.objects.filter(user=request.user))
            return render(request, 'app/emptycart.html',{'totalItem':totalItem})

@login_required
def buy_now(request):
 return render(request, 'app/buynow.html')

@method_decorator(login_required, name="dispatch")
class UserProfileView(View):
    def get(self,request):
        totalItem = 0
        totalItem = len(Cart.objects.filter(user=request.user))
        form = UserProfileForm()
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary', "totalItem" : totalItem})

    def post(self,request):
        form = UserProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.add_message(request, messages.INFO,'Profile Updated Successfully!')
        totalItem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary', "totalItem" : totalItem})


@login_required
def address(request):
    ctm =Customer.objects.filter(user=request.user)
    totalItem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/address.html',{'customer':ctm,'active':'btn-primary', 'totalItem': totalItem})

@login_required
def orders(request):
    orders = Order_Place.objects.filter(user=request.user)
    totalItem = len(Cart.objects.filter(user=request.user))
    context = {
        "orders" : orders,
        "totalItem" : totalItem
    }
    return render(request, 'app/orders.html', context)


def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Samsung' or data == 'Redmi' or data == 'Infinix' or data == 'Oppo':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below10000' :
        mobiles = Product.objects.filter(category='M').filter(discount_price__lt=10000)    
    elif data == 'above10000' :
        mobiles = Product.objects.filter(category='M').filter(discount_price__gte=10000)    
    totalItem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/mobile.html',{'mobiles':mobiles, 'totalItem':totalItem})

class UserRegistration(View):
    def get(self,request):
        form = UserRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Registered Successfully!')
        totalItem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/customerregistration.html', {'form':form, 'totalItem':totalItem})

@login_required        
def checkout(request):
    user = request.user
    address = Customer.objects.filter(user = user)
    cart_items = Cart.objects.filter(user = user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_products = [ p for p in Cart.objects.all() if p.user == user]
    if cart_products:
        for cart_product in cart_products:
            amount = amount + (cart_product.product.discount_price*cart_product.quantity)
        total_amount = amount + shipping_amount
    
    totalItem = len(Cart.objects.filter(user=request.user))
    context = {
        "address" : address,
        "cart_items" : cart_items,
        "total_amount" : total_amount,
        "totalItem" : totalItem
    }
    return render(request, 'app/checkout.html', context)

@login_required
def paymentdone(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    carts = Cart.objects.filter(user=user)
    for cart in carts:
        Order_Place(user=user, customer=customer, product=cart.product, quantity=cart.quantity).save()
        cart.delete()
    return redirect('orders')

@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id'] 
        print('prod_id : ',prod_id)   
        cart = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        print("Cart : ", cart)
        cart.quantity += 1
        cart.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_products = [ p for p in Cart.objects.all() if p.user == request.user]
        if cart_products:
            for cart_product in cart_products:
                amount = amount + (cart_product.product.discount_price*cart_product.quantity)
            total_amount = amount + shipping_amount
            data = {
                'quantity': cart.quantity,
                'amount' : amount,
                'total_amount' : total_amount,
            }
            return JsonResponse(data)

@login_required
def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET.get('prod_id', None)   
        cart = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        cart.quantity -= 1
        cart.save()
        amount = 0
        shipping_amount = 70
        total_amount = 0
        cart_products = [p for p in Cart.objects.all() if p.user==request.user]
        for cart_product in cart_products:
            amount += (cart_product.product.discount_price * cart_product.quantity)
        total_amount = amount + shipping_amount
        data = {
            "amount" : amount,
            "total_amount" : total_amount,
            "quantity" : cart.quantity
        }
        return JsonResponse(data)
        
@login_required
def delete_cart(request):
    if request.method == "GET":
        prod_id = request.GET.get('prod_id', None)
        print("prod_id : ",prod_id)
        cart = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        print("__all: " , cart)
        cart.delete()
        amount = 0
        shipping_amount = 70
        total_amount = 0
        cart_products = Cart.objects.filter(user=request.user)
        for cart_product in cart_products:
            amount += (cart_product.product.discount_price * cart_product.quantity)
        total_amount = amount + shipping_amount
        data = {

            "amount" : amount,
            "total_amount" : total_amount,
        }
        return JsonResponse(data)


def topwear(request, data=None):
    if data == None:
        topwears = Product.objects.filter(category='TW')
    elif data == "all":
        topwears = Product.objects.filter(category='TW')
    elif data == "below500":
        topwears = Product.objects.filter(Q(category='TW') & Q(discount_price__lt = 500))
    elif data == "500_1000":
        topwears = Product.objects.filter(Q(category='TW') & Q(discount_price__gte = 500) & Q(discount_price__1t = 1000) )
    elif data == "1000_2000":
        topwears = Product.objects.filter(Q(category='TW') & Q(discount_price__gte = 1000) & Q(discount_price__lte = 2000) )
    elif data == "above2000":
        topwears = Product.objects.filter(Q(category='TW') & Q(discount_price__gt = 2000))
    elif data == "Khade":
        topwears = Product.objects.filter(Q(category='TW') & Q(brand = 'Khade'))
    elif data == "J":
        topwears = Product.objects.filter(Q(category='TW') & Q(brand = 'J.'))
    elif data == "Nee":
        topwears = Product.objects.filter(Q(category='TW') & Q(brand = 'Nee'))
    
    context = {
        'topwears' : topwears
    }

    return render(request, 'app/topwear.html', context)