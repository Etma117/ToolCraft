from import_export import fields, resources
from Inventario.models import Producto

class ProductoResource(resources.ModelResource):
    id = fields.Field(column_name='ID', attribute='id')
    nombre = fields.Field(column_name='NOMBRE', attribute='nombre')
    medida = fields.Field(column_name='MEDIDA', attribute='medida')
    codigo_barras = fields.Field(column_name='CODIGO DE BARRA', attribute='codigo_barras')
    codigo_producto = fields.Field(column_name='CODIGO/PRODUCTO', attribute='codigo_producto')
    existencia = fields.Field(column_name='EXISTENCIA', attribute='existencia', default=0)
    precio_venta = fields.Field(column_name='PRECIO/VENTA', attribute='precio_venta')
    precio_compra = fields.Field(column_name='PRECIO/COMPRA', attribute='precio_compra', default=0)
    fecha_creacion = fields.Field(column_name='FECHA DE CREACIÓN', attribute='fecha_creacion')
    imagen = fields.Field(column_name='IMAGEN', attribute='imagen')

    class Meta:
        model = Producto
        fields = ('id','nombre', 'medida', 'codigo_barras', 'codigo_producto', 'existencia', 'precio_venta', 'precio_compra', 'fecha_creacion', 'imagen')
        #import_id_fields = ('codigo_producto',)  # Campo único para identificar los productos

        column_name_map = {
            'ID': 'id',
            'NOMBRE': 'nombre',
            'MEDIDA': 'medida',
            'CODIGO DE BARRA': 'codigo_barras',
            'CODIGO/PRODUCTO': 'codigo_producto',
            'EXISTENCIA': 'existencia',
            'PRECIO/VENTA': 'precio_venta',
            'PRECIO/COMPRA': 'precio_compra',
            'FECHA DE CREACIÓN': 'fecha_creacion',
            'IMAGEN': 'imagen',
        }