from django.http import  JsonResponse
from django.shortcuts import redirect, render
from .form import CustomUserForm
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import json

# Create your views here.
def home(request):
    product=Product.objects.filter(trending=1)
    return render(request,'shop/index.html',{'product':product})
def cart_page(request):
    if request.user.is_authenticated:
        cart= Card.objects.filter(user=request.user)
        return render(request,"shop/cart.html",{"cart":cart})

    else:
        return redirect('/')

def favviewpage(request):
    if request.user.is_authenticated:
        fav= Favourite.objects.filter(user=request.user)
        return render(request,"shop/fav.html",{"fav":fav})
    else:
         return redirect('/')

  
 
    
   
def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged Out Successfully...!")
        return redirect('/')
def add_to_cart(request):
    if request.headers.get('X-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
           # print(request.user.id)
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Card.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product Already In Cart'},status=200)
                else:
                    if product_status.quentity>=product_qty:
                        Card.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'A Product Add Cart'},status=200)
                    else:
                        return JsonResponse({'status':'A Product Not Available'},status=200)         
            return JsonResponse({'status':'Product Add to Cart'},status=200)

           
        else:
            return JsonResponse({'status':'Login To Add Cart'},status=200)
    else:
 
       return JsonResponse({'status':'Invalid Access'},status=200)
   

def fav_page(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_id=data['pid']
      product_status=Product.objects.get(id=product_id)
      if product_status:
         if Favourite.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Favourite'}, status=200)
         else:
          Favourite.objects.create(user=request.user,product_id=product_id)
          return JsonResponse({'status':'Product Added to Favourite'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Favourite'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)
   
   
def remove_cart(request,cid):
  cartitem=Card.objects.get(id=cid)
  cartitem.delete()
  return redirect("/cart")    
def remove_fav(request,cid):
  favitem=Favourite.objects.get(id=cid)
  favitem.delete()
  return redirect("/favviewpage")  
 
 
def fav_page(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_id=data['pid']
      product_status=Product.objects.get(id=product_id)
      if product_status:
         if Favourite.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Favourite'}, status=200)
         else:
          Favourite.objects.create(user=request.user,product_id=product_id)
          return JsonResponse({'status':'Product Added to Favourite'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Favourite'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)


def login_page(request):
    if request.method=='POST':
        name=request.POST.get('username')
        pwd=request.POST.get('password')
        user=authenticate(request,username=name,password=pwd)
        if user is not None:
            login(request,user)
            messages.success(request,"Logged In Successfully...!")
            return redirect('/')
        else:
            messages.error(request,"Invalide User Name and Password")
            return redirect('/login')
    return render(request,"shop/login.html")
def regester(request):
    form=CustomUserForm()
    if request.method=='POST':
      form=CustomUserForm(request.POST)
      if form.is_valid():
          form.save()
          messages.success(request,"Regester Success Login Now....!")
          return redirect('/login')      
              
    return render(request,'shop/regester.html',{'form':form})
 
def collection(request):
  catagory=Category.objects.filter(states=0)
  return render(request,"shop/collection.html",{"catagory":catagory})



def collectionviews(request, name):
    if Category.objects.filter(states=0, name=name).exists():
        product = Product.objects.filter(category__name=name)
        return render(request, "shop/productes/index.html", {"product": product,"category":name})
    else:
        messages.warning(request, "No Such Category Found")
        return redirect('coll')

def product_details(request,cname,pname):
    if (Category.objects.filter(states=0, name=cname)):
        if(Product.objects.filter(name=pname,states=0)):
            product=Product.objects.filter(name=pname,states=0).first()
            return render(request,"shop/productes/product_detail.html",{"product":product})
        else:
             messages.error(request,"Such Product Not Found")    
             return redirect('collection')
    else:
        messages.error(request,"No Such Category Found")    
        return redirect('collection')
    