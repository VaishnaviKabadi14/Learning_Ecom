from datetime import time
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from store.models.product import Product
from store.models.order import Customer_order
from store.models.sign_up import Sign_up
from store.models.payment import Payment
from store.middleware.auth import auth_middleware
import razorpay
from e_shop.settings import KEY_ID, KEY_SECRET

# Initialize Razorpay client
client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))

class Order(View):
    @method_decorator(auth_middleware)
    def get(self, request):
        customer_id = request.session.get('id')
        customer = get_object_or_404(Sign_up, id=customer_id)
        cart = request.session.get('cart', {})
        orders = Customer_order.objects.filter(user=customer)
        action = request.GET.get('action')
        products = Product.get_product_By_ids(list(cart.keys()))

        # Calculate total amount
        amount = sum(product.product_price * cart[str(product.id)] for product in products)

        order = None
        payment = None
        error = None  # Initialize error variable

        # Check if customer ID exists
        if customer.id is None:
            return redirect("homepage")

        if action == 'create_payment':
            currency = "INR"
            notes = {
                "email": customer.email,
                "name": customer.name
            }
            receipt = f"PerfectITSolution-{int(time())}"
            order = client.order.create({
                'receipt': receipt,
                'notes': notes,
                'amount': amount * 100,  # Razorpay requires amount in paise
                'currency': currency,
            })

            payment = Payment()
            payment.user = customer
            payment.product = products
            payment.order_id = order.get('id')
            payment.save()

        # Prepare context for rendering
        context = {
            'orders': orders,
            'order': order,
            'payment': payment,
            'user': customer,
            'error': error,
            'total_price': amount,  # Pass the total price to the template
        }

        return render(request, 'order.html', context)


    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer_id = request.session.get('id')
        cart = request.session.get('cart', {})
        products = Product.get_product_By_ids(list(cart.keys()))

        # Fetch the existing user object from the database
        user = get_object_or_404(Sign_up, id=customer_id)

        for product in products:
            order = Customer_order(
                product=product,
                user=user,  # Use the retrieved user object
                quantity=cart.get(str(product.id)),
                price=product.product_price,
                address=address,
                phone=phone
            )
            order.save()

        # Clear cart after order
        request.session['cart'] = {}

        return render(request, 'order.html', {'orders': Customer_order.objects.filter(user=user)})


@csrf_exempt
def verifyPayment(request):
    if request.method == "POST":
        data = request.POST
        try:
            client.utility.verify_payment_signature(data)
            razorpay_order_id = data['razorpay_order_id']
            razorpay_payment_id = data['razorpay_payment_id']

            payment = Payment.objects.get(order_id=razorpay_order_id)
            payment.payment_id = razorpay_payment_id
            payment.status = True
            payment.save()

            return redirect('order')

        except Exception as e:
            return HttpResponse("Invalid Payment Details")

