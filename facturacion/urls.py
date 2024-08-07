from django.urls import path, include
from . import views


urlpatterns = [
    path('productos/', views.producto, name="productos"),
    path('factura/', views.factura, name="facturas"),
    path('', views.home, name="home"),
    path('productos/<int:product_id>/', views.modificar, name="modificar")
]