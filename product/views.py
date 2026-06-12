from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from .decorators import verified_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout
from django.views import View
from .models import Product
from .forms import ProductForm
from django.http import JsonResponse
def main(request):
    return render(request, 'index.html')
#@verified_required
def product_list(request):
    products=Product.objects.all()
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
def product_delete(request, pk):
    if request.method=='POST':
        product=get_object_or_404(Product, pk=pk)
        product.delete()
        return JsonResponse({"success": True, "id": pk})
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
                "sell_price": product.name,
                "buy_price": product.buy_price
            })
        return redirect ("product_list")
    else:
        form=ProductForm(instance=product)
    return render(request, "edit_product.html", {"form": form, "product": product})
def search_product(request):
    query=request.GET.get('q')
    status=request.GET.get('status')
    products=Product.objects.all()
    if query:
        products=products.filter(__icontains=query)
    if status:
        products=[p for p in products if p.status==status]
    context={"request": request, "products": products}
    return redirect(request, "product_list.html", context)
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
            form.save()
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


