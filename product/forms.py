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
class CSVForm(forms.ModelForm):
    csv_file=forms.FileField(label="CSV-файл", help_text="формат: name, buy_price,", "sell_price, source_sell, source_buy")
def clean_csv_file(self):
    file=self.cleaned_data["csv_file"]
    if not file.name.endswith(".csv"):
        raise forms.ValidationError("Загрузите файл с расширением .csv")
    return file
