from django.shortcuts import render, redirect
from django.views import View
from store.models.product import Product
from store.models.category import Category
class Index(View):
    def get(self,request):
        products = Product.objects.all()
        categories=Category.objects.all()

        category_id = request.GET.get('category_id')
        if category_id:
            products = Product.objects.filter(category=category_id)
        data={
            'products':products,
            'categories':categories
        }
        return render(request,'index.html',data)


    def post(self,request):
        product_id = request.POST.get('product_id')
        remove=request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            qty = cart.get(product_id)
            if qty:
                if remove:
                    if qty <= 1:
                        cart.pop(product_id)
                    else:
                        cart[product_id] = qty - 1
                else:
                    cart[product_id] = qty + 1
            else:
                cart[product_id]=1
        else:
            cart = {}
            cart[product_id] = 1
        request.session['cart']=cart
        print("Cart Data",cart)
        return redirect('homepage')


