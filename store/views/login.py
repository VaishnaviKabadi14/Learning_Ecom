from django.shortcuts import render, redirect

from django.views import View
from store.models.sign_up import Sign_up
class Login(View):
    def get(self,request):
        return render(request,'login.html')


    def post(self,request):
        temp=False
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = Sign_up.objects.get(email=email)
            if user:
                if password == user.password:
                    request.session['name']=user.name
                    request.session['id']=user.id
                    return redirect('homepage')
                else:
                    temp=True

        except:
            pass

        return render(request,'login.html',{'temp':temp})


def logout(request):
    request.session.clear()
    return redirect('login')