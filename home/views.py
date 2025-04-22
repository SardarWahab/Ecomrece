from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Store, Product, Cart, CartItem, Order, OrderItem, Payment
from django.utils.text import slugify

import uuid

# Home Page
def home(request):
    products = Product.objects.all()
    return render(request, 'auth/home.html', {'products': products})

def about_view(request):
    return render(request, 'About.html')

def contact_view(request):
    return render(request, 'contact.html')

# Store Creation
@login_required
def create_store(request):
    if request.method == 'POST':
        store_name = request.POST.get('store_name')
        if store_name and not hasattr(request.user, 'store'):
            base_slug = slugify(store_name)
            slug = base_slug
            counter = 1

            # Ensure slug is unique
            while Store.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            try:
                store = Store.objects.create(owner=request.user, store_name=store_name, slug=slug)
                messages.success(request, "Store created successfully!")
                return redirect('store_detail', store_slug=store.slug)
            except Exception as e:
                messages.error(request, f"Error creating store: {e}")

    return render(request, 'store/create_store.html')

# Store Detail
def store_detail(request, store_slug):
    store = get_object_or_404(Store, slug=store_slug)
    store_products = store.products.all()  # Fetch only products related to this store
    return render(request, 'store/store_detail.html', {'store': store, 'store_products': store_products})
# Add Product (For Seller)
@login_required
def add_product(request):
    if request.method == 'POST' and hasattr(request.user, 'store'):
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        if name and price and stock:
            slug = slugify(name)
            Product.objects.create(
                store=request.user.store,
                name=name,
                slug=slug,
                description=description,
                price=price,
                stock=stock
            )
            return redirect('store_detail', slug=request.user.store.slug)
    return render(request, 'store/add_product.html')

# Product Detail
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product_detail.html', {'product': product})

# Add to Cart
from django.urls import reverse  # ✅ Import reverse

@login_required
def add_to_cart(request, product_slug):  # ✅ Use product_slug
    product = get_object_or_404(Product, slug=product_slug)  
    cart, created = Cart.objects.get_or_create(user=request.user)  
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)  
    cart_item.quantity += 1  
    cart_item.save()  

    return redirect(reverse('cart_detail'))  # ✅ Correct redirect


# View Cart
@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    return render(request, 'store/cart.html', {'cart_items': cart_items})

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
    if request.method == "POST":
        total_price = 100  # Example price, replace with actual logic
        unique_slug = slugify(str(uuid.uuid4())[:8])  # Generate a unique slug
        
        order = Order.objects.create(
            customer=request.user,
            total_price=total_price,
            status='Pending',
            slug=unique_slug
        )
        return redirect('order_detail', order_id=order.id)  # Use order ID instead of slug if needed

    # Handle GET requests by rendering a template
    return render(request, "store/order_detail.html")


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