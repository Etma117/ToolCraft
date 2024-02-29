class Venta:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        venta = self.session.get("venta")

        if not venta:
            self.session["venta"]={}
            self.venta = self.session["venta"]
        else:
            self.venta = venta
    
    def agregar(self, producto):
        id = str(producto.id)
        if id not in self.venta.keys():
            self.venta[id]={
                    "producto_id": producto.id,
                    "nombre": producto.nombre,
                    "medida": producto.medida,
                    
                    "precio_venta": float(producto.precio_venta),
                    "acumulado": float(producto.precio_venta),
                    "cantidad": 1,
                }
        else:
            self.venta[id]["cantidad"] +=1
            self.venta[id]["acumulado"] += float(producto.precio_venta) 
        self.guardar_venta()

    def guardar_venta(self):
        self.session["venta"] = self.venta
        self.session.modified = True

    def eliminar (self, producto):
        id = str (producto.id)
        if id in self.venta:
            del self.venta[id]
            self.guardar_venta()
    
    def restar(self, producto):
        id = str(producto.id)  # Mueve esta línea aquí para definir id antes de usarlo
        if id in self.venta.keys() and self.venta[id]["cantidad"] > 0:
            self.venta[id]["cantidad"] -= 1
            self.venta[id]["acumulado"] -= float(producto.precio_venta)

            if self.venta[id]["cantidad"] <= 0:
                self.eliminar(producto)

            self.guardar_venta()

    
    def limpiar (self):
        self.session["venta"]= {}







