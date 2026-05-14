from django.shortcuts import render
from .models import Product
def main(request):
    return render(request, 'index.html')
def status(request):
    product=Product.objects.all().first()
    if product and product.profit_recent()>=10:
        product.status="profitable"
        product.save()
    elif product and product.profit_recent()<10:
        product.status="doubtful"
        product.save()
    else:
        product.status="unprofitable"
        product.save()
    return render(request,'list.html', {"product": product})