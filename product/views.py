from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from .decorators import verified_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout
from django.views import View
from .models import Product
from .forms import ProductForm, CSVForm
from django.http import JsonResponse
import csv, io
from .a import get_price
def lending_page(request):
    return render(request, 'lending_page.html')
def template(request):
    return render(request, "example_template.html")
def main(request):
    return render(request, 'index.html')
#@verified_required
def product_list(request):
    query = request.GET.get('q')
    status = request.GET.get('status')
    products=Product.objects.all()
    if query:
        products=products.filter(name__icontains=query)
    if status:
        products=[p for p in products if p.status==status]
    context={"request": request, "products": products}
    return render(request, 'product_list.html', context)
def login_user(request):
    if request.method=='POST':
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('product_list')
        else:
            return render(request, "login.html", {"error": "Неверные данные"})
    return render(request, "login.html")
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Имя уже занято"})
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect("index")
    return render(request, "register.html")
def login_success(request):
    return render(request, "login_success.html")
def product_delete(request, pk):
    if request.method=='POST':
        product=get_object_or_404(Product, pk=pk)
        product.delete()
    return redirect("product_list")
def edit_product(request, pk):
    product=get_object_or_404(Product, pk=pk)
    if request.method=='POST':
        form=ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return JsonResponse({
                "success": True,
                "id": pk,
                "name": product.name,
                "sell_price": product.sell_price,
                "buy_price": product.buy_price
            })
        return redirect ("product_list")
    else:
        form=ProductForm(instance=product)
    return render(request, "edit_product.html", {"form": form, "product": product})
def user_logout(request):
    logout(request)
    return redirect("index")
def verify_email(request):
    if request.method=="POST":
        email=request.POST.get("email")
        messages.info(request, "Проверьте почту для подтверждения")
        return redirect("login")
    return render(request, "verify_email.html")
#@verified_required
def add_product(request):
    if request.method=='POST':
        form=ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            url=form.cleaned_data.get('url_website')
            if url:
                price=get_price(url)
                if price:
                    product.buy_price=float(price)
            product.save()
            return redirect("product_list")
    else:
        form=ProductForm()
    return render(request, 'add_product.html', {"form": form})
#@verified_required
def sort_status(request):
    selected_status=request.POST.get("status", "profitable")
    PRIORITY_MAP={"profitable": ["profitable", "doubtful", "unprofitable"], "doubtful": ["doubtful", "unprofitable", "profitable"], "unprofitable":["unprofitably", "doubtful", "profitable"]}
    order=PRIORITY_MAP[selected_status]
    products=list(Product.objects.all())
    products.sort(key=lambda p: order.index(p.status))
    return render(request, "product_list.html", {"products": products})
def import_csv(request):
    if request.method == "POST":
        form = CSVForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                file = form.cleaned_data["csv_file"]
                decoded = file.read().decode("utf-8")
                reader = csv.DictReader(io.StringIO(decoded))

                count = 0
                errors = []

                for i, row in enumerate(reader, start=2):
                    name = (row.get("name") or "").strip()
                    buy_price_raw = (row.get("buy-price") or "").strip()
                    sell_price_raw = (row.get("sell_price") or "").strip()

                    if not name or not buy_price_raw or not sell_price_raw:
                        errors.append(f"В строке {i}: пропущены важные поля")
                        continue

                    try:
                        buy_price = float(buy_price_raw)
                        sell_price = float(sell_price_raw)
                    except ValueError:
                        errors.append(f"Строка {i}: цена должна быть числом")
                        continue

                    Product.objects.create(
                        name=name,
                        buy_price=buy_price,
                        sell_price=sell_price,
                        source_buy=row.get("source_buy", ""),
                        source_sell=row.get("source_sell", "")
                    )
                    count += 1

                return render(
                    request,
                    "csv.html",
                    {
                        "form": form,
                        "success": count,
                        "errors": "; ".join(errors) if errors else None
                    }
                )

            except Exception:
                return render(
                    request,
                    "error_pages/error_500.jinja2",
                    status=500
                )
        else:
            return render(
                request,
                "error_pages/error_403.jinja2",
                status=403
            )

    else:
        form = CSVForm()
        return render(request, "csv.html", {"form": form})



