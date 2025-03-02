from django.urls import path
from .views import (
    home, create_store, store_detail, add_product, product_detail,
    add_to_cart, cart_detail, remove_from_cart, place_order, order_detail,
    mark_order_delivered, confirm_payment
)

urlpatterns = [
    path('', home, name='home'),
    path('store/create/', create_store, name='create_store'),
    path('store/<int:store_id>/', store_detail, name='store_detail'),
    path('product/add/', add_product, name='add_product'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/remove/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('order/place/', place_order, name='place_order'),
    path('order/<int:order_id>/', order_detail, name='order_detail'),
    path('order/delivered/<int:order_id>/', mark_order_delivered, name='mark_order_delivered'),
    path('order/payment/<int:order_id>/', confirm_payment, name='confirm_payment'),
]
