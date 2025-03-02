from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Store, Product, Cart, CartItem, Order, OrderItem, Payment

# Home Page
def home(request):
    products = Product.objects.all()
    return render(request, 'auth/home.html', {'products': products})

# Store Creation
@login_required
def create_store(request):
    if request.method == 'POST':
        store_name = request.POST.get('store_name')
        if store_name and not hasattr(request.user, 'store'):
            Store.objects.create(owner=request.user, store_name=store_name)
            return redirect('store_detail', store_id=request.user.store.id)
    return render(request, 'home/create_store.html')

# Store Detail
def store_detail(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    products = store.products.all()
    return render(request, 'home/store_detail.html', {'store': store, 'products': products})

# Add Product (For Seller)
@login_required
def add_product(request):
    if request.method == 'POST' and hasattr(request.user, 'store'):
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        if name and price and stock:
            Product.objects.create(
                store=request.user.store,
                name=name,
                description=description,
                price=price,
                stock=stock
            )
            return redirect('store_detail', store_id=request.user.store.id)
    return render(request, 'home/add_product.html')

# Product Detail
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'home/product_detail.html', {'product': product})

# Add to Cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_detail')

# View Cart
@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    return render(request, 'home/cart.html', {'cart_items': cart_items})

# Remove from Cart
@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if cart_item.cart.user == request.user:
        cart_item.delete()
    return redirect('cart_detail')

# Checkout & Place Order
@login_required
def place_order(request):
    cart = get_object_or_404(Cart, user=request.user)
    if cart.items.exists():
        total_price = sum(item.product.price * item.quantity for item in cart.items.all())
        order = Order.objects.create(customer=request.user, total_price=total_price, status='Pending')

        for item in cart.items.all():
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)

        cart.items.all().delete()  # Clear the cart after order
        return redirect('order_detail', order_id=order.id)

    return redirect('cart_detail')

# Order Detail
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    order_items = order.order_items.all()
    return render(request, 'home/order_detail.html', {'order': order, 'order_items': order_items})

# Mark Order as Delivered (For Admin/Seller)
@login_required
def mark_order_delivered(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.user.is_staff or request.user == order.customer:
        order.status = 'Delivered'
        order.save()
    return redirect('order_detail', order_id=order.id)

# Payment Confirmation (Cash on Delivery)
@login_required
def confirm_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    Payment.objects.create(order=order, status='Pending')  # Since it's Cash on Delivery
    return redirect('order_detail', order_id=order.id)
