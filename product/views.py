from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from .decorators import verified_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout
from .models import Product
def main(request):
    return render(request, 'index.html')
#@verified_required
def product_list(request):
    products=Product.objects.all()
    for product in products:
        if product.profit_recent>=10:
            product.status="profitable"
        elif 0<product.profit_recent<10:
            product.status="doubtful"
        else:
            product.status="unprofitable"
        product.save()
    return render(request, 'product_list.html', {"products": products})
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
        name=request.POST.get("name")
        buy_price=request.POST.get("buy_price")
        sell_price=request.POST.get("sell_price")
        product=Product.objects.create(name=name,
                               buy_price=buy_price,
                               sell_price=sell_price)
        return redirect("product_list")
    return render(request, 'add_product.html')
#@verified_required
def sort_status(request):
    selected_status=request.POST.get("status", "profitable")
    PRIORITY_MAP={"profitable": ["profitable", "doubtful", "unprofitable"], "doubtful": ["doubtful", "unprofitable", "profitable"], "unprofitable":["unprofitably", "doubtful", "profitable"]}
    order=PRIORITY_MAP[selected_status]
    products=list(Product.objects.all())
    products.sort(key=lambda p: order.index(p.status))
    return render(request, "product_list.html", {"products": products})


