# Generated by Django 4.2 on 2024-03-05 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventario', '0003_alter_producto_codigo_producto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='precio_compra',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Precio de Compra'),
        ),
    ]