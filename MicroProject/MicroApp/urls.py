from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('reg',views.regester,name='reg' ),
    path('login',views.login_page,name="login"),
    path('logout',views.logout_page,name="logout"),
    path('cart',views.cart_page,name="cart"),
    path('cart',views.cart_page,name="cart"),
    path('fav',views.fav_page,name="fav"),
    path('favviewpage',views.favviewpage,name='favviewpage'),
    path('remove_fav/<str:cid>',views.remove_fav,name="remove_fav"),
    
    path('remove_cart/<str:cid>',views.remove_cart,name="remove_cart"),
    path('fav/<str:cid>',views.fav_page,name="fav"),
    path('collection',views.collection,name='collection' ),
    path('collection/<str:name>', views.collectionviews,name='collection'),
    path('collection/<str:cname>//<str:pname>', views.product_details,name='product_details'),
    path('addtocart',views.add_to_cart,name="addtocart"),





]