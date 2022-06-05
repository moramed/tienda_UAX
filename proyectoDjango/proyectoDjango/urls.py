"""proyectoDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from aplicacionGeneral.views import registro, login_request, logout_request, inicio, agregar_producto, \
    restar_producto, eliminar_producto, limpiar_carrito, hacer_pedido, ver_pedidos, ver_detalle  # logout_request,
from django.contrib.auth.views import LoginView, LogoutView, logout_then_login
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls, name='administrar'),
    path('',inicio, name = 'inicio'),
    path('registro/',registro, name='registro'),
    path('login/',login_request, name='login'),
    path('salir/',logout_request, name='salir'),
    path('agregar/<int:servicio_id>',agregar_producto, name='agregar'),
    path('eliminar/<int:servicio_id>',eliminar_producto, name='eliminar'),
    path('restar/<int:servicio_id>',restar_producto, name='restar'),
    path('limpiar/',limpiar_carrito, name='limpiar'),
    path('pedido/',hacer_pedido, name='pedido'),
    path('ver_pedidos/',ver_pedidos, name='ver_pedidos'),
    path('ver_detalle/<int:pedido_id>',ver_detalle, name='ver_detalle'),
]