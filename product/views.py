from django.shortcuts import render, get_object_or_404
from .models import Product
def main(request):
    return render(request, 'index.html')
def status(request):
    product=Product.objects.all().first()
    if product.profit_recent()>=0.10:
        return Product.order_by()