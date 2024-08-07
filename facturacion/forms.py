from django import forms
from .models import Cliente, Producto, TipoPago

class CrearNuevaFactura(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre_producto', 'enlace_temu', 'cantidad', 'precio', 'tipo_pago']

        def __init__(self, *args, kwargs):
            super().__init__(*args, *kwargs)
            self.fields['tipo_pago',].queryset = TipoPago.objects.all().order_by('tipo')

class BuscarCliente(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['numero_wsp',]

class ActualizarEstado(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['encargado', 'recibido', 'entregado',]

class ModificarProducto(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['factura', 'nombre_producto', 'enlace_temu', 'cantidad', 'precio', 'tipo_pago', 'encargado', 'recibido', 'entregado',]