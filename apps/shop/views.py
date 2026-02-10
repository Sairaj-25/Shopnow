from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import *

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Customerform
from .forms import CustomerForm
from django.views import View
import razorpay
from django.conf import settings
from django.http import HttpResponseBadRequest


# Create your views here.




def home(request):

    products = Product.objects.filter(is_active=True)

    # Group products by category
    grouped_products = {}
    for product in products:
        category = product.category
        if category not in grouped_products:
            grouped_products[category] = []

        grouped_products[category].append(product)

    # If the user is authenticated, fetch their cart items and quantities
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = []

    cart_quantities = {item.product.id: item.quantity for item in cart_items}

    # Add quantity information directly in the context for each product
    for product in products:
        product.user_quantity = cart_quantities.get(product.id, 0)


    context = {
        'products': grouped_products,
        'cart_quantities': cart_quantities,
        }
    return render(request,'Index.html', context)

def login_user(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request,'Login.html', {'errormsg': 'Invalid username or password'})

    return render(request, 'Login.html', context)

def register_user(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('pass1')
        password2 = request.POST.get('pass2')

        if password1 != password2:
            return render(request,'Register.html',{'errormsg':'Passwords do not match'})
        
        if User.objects.filter(username=email).exists():
            return render(request, 'Register.html', {'errormsg': 'Email is already registered.'})

        user = User.objects.create_user(username=email,password=password1)
        user.save()

        # Auto Login after successful registration
        user = authenticate(request, username=email, password=password1)
        login(request, user)

        messages.success(request, 'Welcome! Your account has been created.')
        return redirect('/')
    
    return render(request, 'register.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def forgot_pass(request):
    context = {}
    
    if request.method == "POST":
        uname = request.POST.get('uname')
        upass = request.POST.get('upass')
        upass2 = request.POST.get('upass2')
        
        if not uname or not upass or not upass2:
            context['errormsg'] = "All fields are required."
            return render(request, 'Forgot_Pass.html', context)
        
        if upass != upass2:
            context['errormsg'] = "Passwords do not match."
            return render(request, 'Forgot_Pass.html', context)
        
        try:
            user = User.objects.get(username=uname)
        except User.DoesNotExist:
            context['errormsg'] = "User does not exist."
            return render(request, 'Forgot_Pass.html', context)
        
        user.set_password(upass)
        user.save()
        messages.success(request, "Your password has been successfully reset. Please login with your new password.")
        return redirect('login',)
    
    return render(request, 'Forgot_Pass.html', context)


def all_products(request,id):
    category_name = get_object_or_404(Category, id = id)
    products = Product.objects.filter(category=category_name)

    # If the user is authenticated, fetch their cart items and quantities
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = []

    cart_quantities = {item.product.id: item.quantity for item in cart_items}

    # Add quantity information directly in the context for each product
    for product in products:
        product.user_quantity = cart_quantities.get(product.id, 0)
    
    context = {
        'category': category_name,
        'products': products,
        'cart_items':cart_items,
    }
    return render(request, 'See-all.html', context)

def catfilter(request, category_id):
    categories = Category.objects.all()
    category = get_object_or_404(Category,id=category_id)
    products = Product.objects.filter(category=category)

    # If the user is authenticated, fetch their cart items and quantities
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = []

    cart_quantities = {item.product.id: item.quantity for item in cart_items}

    # Add quantity information directly in the context for each product
    for product in products:
        product.user_quantity = cart_quantities.get(product.id, 0)

    context = {
        'categories': categories,
        'products':products,
        'category':category,
        'cart_items':cart_items,
    }
    return render(request, 'Category_products.html', context)

def searchfilter(request):
    query = request.GET.get('query','')
    products = Product.objects.filter(name__icontains = query)

    
    # If the user is authenticated, fetch their cart items and quantities
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = []

    cart_quantities = {item.product.id: item.quantity for item in cart_items}

    # Add quantity information directly in the context for each product
    for product in products:
        product.user_quantity = cart_quantities.get(product.id, 0)

    context = {
        'products':products,
        'cart_items':cart_items,
        'query': query,
    }
    return render(request, 'Search.html', context)


def product_info(request,pid):
    product = get_object_or_404(Product, id=pid)
    context = {
        'product': product,
    }
    return render(request,'Product-info.html',context)


def cart(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.get_total_price() for item in cart_items)
    total_quantity = sum(item.quantity for item in cart_items)
    # Example flat shipping cost
    if cart_items.exists():   
        if total > 199:
            delivery_charges = 0
        else:
            delivery_charges = 25
    else :
        delivery_charges = 0
    handling_charges = 10 if cart_items.exists() else 0
    grand_total = total + delivery_charges + handling_charges

    context = {
        'cart_items': cart_items,
        'Total': total,
        'total_quantity': total_quantity,
        'delivery_charges': delivery_charges,
        'handling_charges': handling_charges,
        'GrandTotal': grand_total,
    }
    return render(request, 'Cart.html', context)


@csrf_exempt
def get_cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        cart_data = [{"product_id": item.product.id, "quantity": item.quantity} for item in cart_items]
        return JsonResponse({"cart_items": cart_data})
    return JsonResponse({"cart_items": []})

def login_check(request):
    return JsonResponse({"isAuthenticated": request.user.is_authenticated})

def about(request):
    return render(request, 'About.html')

def contact(request):
    return render(request, 'Contact.html')

def policy(request):
    return render(request, 'Policy.html')

# later: save to DB or send email
def feedback(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        rating = request.POST.get("rating")
        message = request.POST.get("message")
    return render(request, 'Feedback.html')


@csrf_exempt  # CSRF handled in frontend
@login_required
def add_to_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        product_id = data.get("product_id")
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if created:
            cart_item.quantity = 1
        cart_item.save()
        return JsonResponse({"message": "Added to cart", "quantity": cart_item.quantity})
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
@login_required
def update_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        product_id = data.get("product_id")
        action = data.get("action")
        cart_item = get_object_or_404(CartItem, user=request.user, product_id=product_id)
        
        if action == "increment":
            cart_item.quantity += 1
        elif action == "decrement" and cart_item.quantity > 1:
            cart_item.quantity -= 1
        elif action == "decrement":
            cart_item.delete()
            return JsonResponse({"message": "Removed from cart", "quantity": 0})
        
        cart_item.save()
        return JsonResponse({"message": "Cart updated", "quantity": cart_item.quantity})
    return JsonResponse({"error": "Invalid request"}, status=400)

# Update the quantity For Cart.html (increment or decrement)
def update_quantity(request, product_id, action):
    cart_item = get_object_or_404(CartItem, user=request.user, product_id=product_id)
    if action == 'increment':
        cart_item.quantity += 1
    elif action == 'decrement':
        cart_item.quantity -= 1
    cart_item.save()
    # Redirect back to the same page
    return redirect(request.META.get('HTTP_REFERER', '/'))

@csrf_exempt
def remove_from_cart(request, product_id):
    if request.method == "DELETE":
        cart_item = get_object_or_404(CartItem, user=request.user, product_id=product_id)
        cart_item.delete()

        # Get updated cart items
        cart_items = CartItem.objects.filter(user=request.user)
        total = sum(item.get_total_price() for item in cart_items)
        total_quantity = sum(item.quantity for item in cart_items)  

        # Determine delivery charges
        if total > 199:
            delivery_charges = 0
        else:
            delivery_charges = 25 if cart_items.exists() else 0
        
        # Handling charges
        handling_charges = 10 if cart_items.exists() else 0

        grand_total = total + delivery_charges + handling_charges

        # Prepare JSON response
        cart_data = {
            "cart_items": [{"product_id": item.product.id, "quantity": item.quantity} for item in cart_items],
            'Total': total,
            'total_quantity':total_quantity,
            'delivery_charges': delivery_charges,
            'handling_charges': handling_charges,
            'GrandTotal': grand_total,
        }
        
        return JsonResponse(cart_data)  # <- Missing in your code

@login_required
def profile(request):
    # for customer profile
    user = request.user
    customer = Customer.objects.filter(user=user)
    
    context = {
        'user': user,
        'customer': customer
        }
    return render(request, 'Profile.html', context)

def place_order(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user
            customer.save()
            messages.success(request, "Customer details saved successfully!")
            return render(request, "Payment.html")
        messages.error(request, "Invalid form data. Please try again.")
    
    return render(request, "Place_order.html", {"form": CustomerForm()})

def make_payment(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)

    # Calculate delivery and handling charges
    delivery_charges = 0 if total_price > 199 else 25
    handling_charges = 10
    grand_total = total_price + delivery_charges + handling_charges

    # Initialize Razorpay Client
    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

    # Always create a Razorpay order before rendering the template
    order_data = {
        "amount": int(grand_total * 100),  # Convert to paisa
        "currency": "INR",
        "payment_capture": 1
    }
    order = client.order.create(data=order_data)

    # Save order details in the database
    new_order, created = Order.objects.get_or_create(
        user=request.user,
        order_id=order["id"],
        defaults={"amount": grand_total}
    )

    # If the request is a POST request (payment attempt), return JSON response
    if request.method == "POST":
        return JsonResponse({
            "order_id": order["id"],
            "razorpay_key": settings.RAZOR_KEY_ID,
            "razoramount": int(grand_total * 100),
        }, status=200)

    context = {
        "cart_items": cart_items,
        "total": total_price,
        "delivery_charges": delivery_charges,
        "handling_charges": handling_charges,
        "grand_total": grand_total,
        "razorpay_key": settings.RAZOR_KEY_ID,  # Pass key dynamically
        "razoramount": int(grand_total * 100),
        "order_id": order["id"],  # Order ID will always be available
        "callback_url": request.build_absolute_uri('/payment_done/'),
    }

    return render(request, "Payment.html", context)


@csrf_exempt
def payment_done(request):
    if request.method == "POST":
        order_id = request.POST.get("razorpay_order_id")
        payment_id = request.POST.get("razorpay_payment_id")
        print(f"Payment Callback Received: Order ID - {order_id}, Payment ID - {payment_id}")  # Debugging

        if not order_id or not payment_id:
            return JsonResponse({"error": "Invalid payment details received."}, status=400)

        try:
            order = Order.objects.get(order_id=order_id)
            order.payment_id = payment_id
            order.status = "Paid"
            order.save()
            print(f"Order Updated as Paid: {order.id}")  # Debugging

            # Fetch all cart items for the user
            cart_items = CartItem.objects.filter(user=request.user)

            # Create order items for each cart item
            order_items = []
            for cart_item in cart_items:
                order_item, created = OrderItem.objects.get_or_create(
                    user=request.user,
                    order=order,
                    product=cart_item.product,
                    defaults={"quantity": cart_item.quantity},
                )
                order_items.append(order_item)

            # Clear user's cart
            cart_items.delete()
            orders = Order.objects.filter(user=request.user).order_by('-created_at')
            context = {
                "orderitems": order_items,
                "order": order
                }
            return redirect('order')  # Redirect to orders page after successful payment

        except Order.DoesNotExist:
            print("Order Not Found!")  # Debugging
            return JsonResponse({"error": "Order not found!"}, status=404)

        except Exception as e:
            print(f"Error: {str(e)}")  # Debugging
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=400)

@login_required
def my_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')

    context = {
        'orders': orders
    }
    return render(request, 'Orders.html', context)

def delete_order_item(request,item_id):
    pass