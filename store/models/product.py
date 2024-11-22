from django.db import models
from . category import Category

class Product(models.Model):
    product=models.CharField(max_length=25)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    product_description=models.CharField(max_length=150)
    product_price=models.IntegerField()
    product_img=models.ImageField(upload_to="img/")


    def __str__(self):
        return self.product
    @staticmethod
    def get_product_By_ids(ids):
        return Product.objects.filter(id__in=ids)

