from django.db import models

# Create your models here.
class TipoPago(models.Model):
    tipo = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tipo

class Cliente(models.Model):
    numero_wsp = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return self.numero_wsp


class Producto(models.Model):
    fecha = models.DateTimeField(auto_now=True)
    nombre_producto = models.CharField(max_length=200)
    enlace_temu = models.CharField(max_length=300)
    cantidad = models.IntegerField(default=1)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tipo_pago = models.ForeignKey(TipoPago, on_delete=models.DO_NOTHING, to_field='tipo')
    encargado = models.BooleanField(default=False)
    recibido = models.BooleanField(default=False)
    entregado = models.BooleanField(default=False)
    factura = models.ForeignKey(Cliente, on_delete=models.CASCADE, to_field='numero_wsp')

    @property
    def total(self):
        return self.precio * self.cantidad
    

    def fecha_formateada(self):
        return self.fecha.strftime('%d/%m/%Y %H:%M')
    

