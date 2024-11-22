import datetime

from django.db import models
from store.models.product import Product
from store.models.sign_up import Sign_up
class Customer_order(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(Sign_up,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=50,default='')
    phone = models.CharField(max_length=12,default='')
    date = models.DateField(default=datetime.datetime.today())
    status = models.BooleanField(default=False)
    @staticmethod
    def get_order_by_customer(customer):
        return Customer_order.objects.filter(user=Customer)