"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import product.views as views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name='main'),
    path('products/all/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name="add_product"),
    path('products/sort/', views.sort_status, name="sort_status"),
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='user_logout'),
    path('login_success/', views.login_success, name='login_success'),
    path('verify-email/', views.verify_email, name="verify_email"),
    path('products/delete/<int:pk>', views.product_delete, name="product_delete"),
    path('products/edit/<int:pk>', views.edit_product, name="edit_product"),
    path('a/', views.template, name='template')
]
