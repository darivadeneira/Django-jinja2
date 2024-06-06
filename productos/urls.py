from django.urls import path
from . import views

urlpatterns = [
    # URLs de vistas normales
    path('', views.listar_productos, name='listar_productos'),
    path('agregar/',views.agregar_producto,name='agregar_producto'),
    path('editarProducto/<id>', views.editar_producto, name='editar_producto'),
    path('eliminarProducto/<id>/',views.eliminarProducto),
    path('importarCsv/', views.importarCsv , name='importar_csv'),
    path('exportarCsv/', views.exportarCsv , name='exportar_csv'), 
]