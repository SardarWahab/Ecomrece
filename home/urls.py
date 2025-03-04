from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),
    path('store/create/', create_store, name='create_store'),
    path('store/<slug:store_slug>/', store_detail, name='store_detail'),
    path('product/add/', add_product, name='add_product'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('cart/add/<slug:product_slug>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/remove/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('order/place/', place_order, name='place_order'),
    path('order/<slug:order_slug>/', order_detail, name='order_detail'),
    path('order/delivered/<slug:order_slug>/', mark_order_delivered, name='mark_order_delivered'),
    path('order/payment/<slug:order_slug>/', confirm_payment, name='confirm_payment'),
]
