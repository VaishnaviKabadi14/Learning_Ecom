from django.shortcuts import render
from django.views import View
from store.models.product import Product


class Cart(View):
    def get(self, request):
        # Initialize 'cart' as an empty dictionary if it doesn't exist
        cart = request.session.get('cart', {})

        # Check if the cart is not empty before trying to get product IDs
        if cart:
            ids = list(cart.keys())
            products = Product.get_product_By_ids(ids)
        else:
            products = []  # No products if cart is empty

        return render(request, 'cart.html', {'products': products, 'cart': cart})
