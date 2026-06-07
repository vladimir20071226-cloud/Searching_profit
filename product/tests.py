from .errors import InsufficientStockError
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Product
def add_to_cart(product, quantity):
    if quantity>product.stock:
        raise InsufficientStockError(product.name, quantity, product.stock)
def transfer(request, pk):
    product = get_object_or_404(Product, pk=pk)
    quantity = int(request.POST.get("quantity", 1))
    try:
        add_to_cart(product, quantity)
        messages.success(request, f"Товар {product.name} добавлен в корзину")
    except InsufficientStockError as e:
        messages.error(request, str(e))
def test_insufficient_stock_error():
    product=Product(name="Телефон", stock=3)
    try:
        add_to_cart(product, 10)
    except InsufficientStockError as e:
        assert "в наличии" in str(e)