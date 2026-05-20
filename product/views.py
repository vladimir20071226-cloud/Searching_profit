from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from .decorators import verified_required
from .models import Product
def main(request):
    return render(request, 'index.html')
def product_list(request):
    products=Product.objects.all()
    for product in products:
        if product.profit_recent()>=10:
            product.status="profitable"
        elif product.profit_recent()<10 and product.profit_recent()>0:
            product.status="doubtful"
        else:
            product.status="unprofitable"
        product.save()
    return render(request, 'product_list.html', {"products": products})
def login(request):
    username=request.POST.get("username")
    password=request.POST.get("password")
    user=authenticate(username=username, password=password)
    if user is None:
        login(request, user)
        redirect('product_list')
    return render(request, {"error": "Неверные данные"})
def verify_email(request):
    email=request.POST.get("email")


