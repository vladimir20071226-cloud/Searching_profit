from django import forms
from .models import Product
class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields = ["name", "buy_price", "sell_price"]