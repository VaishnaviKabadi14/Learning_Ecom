from django import template
register =template.Library()

@register.filter("is_in_cart")
def is_in_cart(product,cart):
    keys = cart.keys()

    for key in keys:
        #print(type(key),type(product.id))
        if int(key) == product.id:
            return True

    return False


@register.filter("cart_quantity")
def cart_quantity(product, cart):
    keys = cart.keys()
    for key in keys:
        if int(key)==product.id:
            return cart.get(key)


@register.filter("price_total")
def price_total(product, cart):

    return product.product_price * cart_quantity(product,cart)


@register.filter("Total_cart_price")
def Total_cart_price(products, cart):
    sum = 0
    for p in products:
        sum += price_total(p,cart)
    return sum





@register.filter("multiply")
def multiply(qty, price):

    return qty*price