from django.shortcuts import render

from django.views import View
from store.models.sign_up import Sign_up
class Customer(View):
    def get(self,request):
        return render(request,'sign_up.html')


    def post(self,request):
        temp=False
        name=request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            sign=Sign_up(name=name,email=email,password=password)
            sign.save()
            temp=True
        except:
            pass
        return render(request,'sign_up.html',{'temp':temp})