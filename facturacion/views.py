from django.shortcuts import render, redirect
from django.db.models import Q
from .models import TipoPago, Cliente, Producto
from .forms import CrearNuevaFactura, BuscarCliente, ActualizarEstado, ModificarProducto
import json
from django.http import JsonResponse



# Create your views here.
def producto(request):
    if request.method == 'GET':
        producto = Producto.objects.all()
        return render(request, 'productos.html', {
            'producto':producto,
            'estado':ActualizarEstado,
        })
    if request.method == 'POST':
        form_name = request.POST['form_name']
        if form_name == 'form2':
            form = ActualizarEstado(request.POST)
            if form.is_valid():
                encargado = form.cleaned_data['encargado']
                recibido = form.cleaned_data['recibido']
                entregado = form.cleaned_data['entregado']
                objeto = Producto.objects.get(pk=request.POST['id'])
                if entregado:
                    objeto.encargado = entregado
                    objeto.recibido = entregado
                    objeto.entregado = entregado
                if recibido:
                    objeto.encargado = recibido
                    objeto.recibido = recibido
                if encargado:
                    objeto.encargado = encargado
                objeto.save()
                return redirect('/productos/')
        if form_name == 'form1':
                query = request.POST.get('buscar')
                clientes = Cliente.objects.all()
                productos = Producto.objects.all()

                if query:
                    clientes = clientes.filter(
                        Q(numero_wsp__icontains=query)
                    ).values_list('numero_wsp', flat=True)
                    productos = productos.filter(
                        Q(factura__numero_wsp__icontains=clientes) |  # Accediendo al campo numero_wsp del modelo Cliente
                        Q(nombre_producto__icontains=query) |
                        Q(enlace_temu__icontains=query)  
                    )
                return render(request, 'productos.html', {
                    'producto':productos,
                    'estado':ActualizarEstado,
                })
        
    
def home(request):
    return render(request, 'home.html')

def factura(request):
    if request.method == 'GET':
        return render(request, 'factura.html', {
            'factura':CrearNuevaFactura,
        })
    if request.method == 'POST':
        data = json.loads(request.body)
        numero_wsp = data.get('numero_wsp')
        productos_data = data.get('productos')

        cliente, created = Cliente.objects.get_or_create(numero_wsp=numero_wsp)

        for prod in productos_data:
            tipo_pago_instance = TipoPago.objects.get(tipo=prod['tipo_pago'])
            Producto.objects.create(
                nombre_producto=prod['nombre'],
                enlace_temu=prod['enlace_temu'],
                cantidad=prod['cantidad'],
                precio=prod['precio'],
                tipo_pago=tipo_pago_instance,
                factura=cliente
            )
        return JsonResponse({'success': True})

    
def modificar(request, product_id):
    producto = Producto.objects.get(pk=product_id)
    if request.method == 'GET':
        siguiente = producto.pk + 1
        anterior = producto.pk - 1
        modificar = ModificarProducto(instance=producto)
        return render(request, 'modificar.html', {
            'modificar':modificar,
            'producto':producto,
            'anterior':anterior,
            'siguiente':siguiente
            })
    if request.method == 'POST':
        form = ActualizarEstado(request.POST)
        if form.is_valid():
            tipo_pago_instace = TipoPago.objects.get(tipo=request.POST['tipo_pago'])
            cliente_instace = Cliente.objects.get(numero_wsp=request.POST['factura'])
            producto.nombre_producto = request.POST['nombre_producto']
            producto.enlace_temu = request.POST['enlace_temu']
            producto.cantidad = request.POST['cantidad']
            producto.precio = request.POST['precio']
            producto.encargado = form.cleaned_data['encargado']
            producto.recibido = form.cleaned_data['recibido']
            producto.recibido = form.cleaned_data['entregado']
            producto.tipo_pago = tipo_pago_instace
            producto.factura = cliente_instace
            producto.save()
            return redirect('/productos/%s' %producto.pk)




        