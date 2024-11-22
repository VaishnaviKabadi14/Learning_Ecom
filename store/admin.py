from django.contrib import admin
from store.models.product import Product
from store.models.category import Category
from store.models.sign_up import Sign_up
from store.models import Customer_order
from store.models import Payment

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Sign_up)
admin.site.register(Customer_order)
admin.site.register(Payment)