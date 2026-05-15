from django.shortcuts import render, redirect
from .models import Product
def main(request):
    return render(request, 'index.html')
def product_list(request):
    products=Product.objects.all()
    for product in products:
        if product.profit_recent()>=10:
            product.status="profitable"
        elif product.profit_recent()<10:
            product.status="doubtful"
        else:
            product.status="unprofitable"
        product.save()
    return render(request, 'product_list.html', {"products": products})