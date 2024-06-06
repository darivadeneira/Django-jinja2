from django.shortcuts import render,redirect
from .models import Producto
from .forms import CSVUploadForm
import csv
from django.http import HttpResponse


productos = []

def listar_productos(request):
    productos = Producto.objects.all()
    form = CSVUploadForm()
    return render(request, 'listar.html', {'productos': productos,'form': form})

def agregar_producto(request):
    
    nombre = request.POST['textoProducto']
    precio = request.POST['textoPrecio']
    unidad = request.POST['textoUnidad']

       
    precio = precio.replace(',', '.')

    try:
        precio = float(precio)
        precio = f"{precio:.2f}"
    except ValueError:
        productos = Producto.objects.all()
        return render(request, 'listar.html', {'productos': productos,'error': 'El precio debe ser un número decimal.'})

    Producto.objects.create(
        nombre=nombre, precio=precio, cantidad=unidad
    )
    return redirect('/')


def editar_producto(request,id):
    id = request.POST['id']
    nombre = request.POST['textoProducto']
    precio = request.POST['textoPrecio']
    unidad = request.POST['textoUnidad']
    
    precio = precio.replace(',', '.')
    
    try:
        precio = float(precio)
        precio = f"{precio:.2f}"
    except ValueError:
        productos = Producto.objects.all()
        return render(request, 'listar.html', {'productos': productos, 'errorEditar': 'El precio debe ser un número decimal.'})

    producto = Producto.objects.get(id=id)
    producto.nombre = nombre
    producto.precio = precio
    producto.cantidad = unidad
    producto.save()

    return redirect('/')



def eliminarProducto(request, id):
    producto = Producto.objects.get(id=id)
    producto.delete()
    return redirect('/')


def importarCsv(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            
            for row in reader:
                Producto.objects.create(
                    nombre=row['producto'],
                    precio=row['precio'],
                    cantidad=row['cantidad']
                )
            return redirect('/')
    return redirect('/')

def exportarCsv(request):
    productos = Producto.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ProductosLista.csv"'

    writer = csv.writer(response)
    writer.writerow(['nombre', 'precio', 'cantidad'])
    for producto in productos:
        writer.writerow([ producto.nombre, producto.precio, producto.cantidad])

    return response