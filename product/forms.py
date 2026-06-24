from django import forms
from .models import Product
class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields = ["name", "buy_price", "sell_price", "url_website"]
        labels={
            "name":"Название товара",
            "buy_price": "Цена покупки",
            "sell_price": "Цена продажи",
            "url_website": "Ссылка на сайт"
        }