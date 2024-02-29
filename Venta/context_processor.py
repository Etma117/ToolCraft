from decimal import Decimal

def total_venta(request):
    total = float(0)
    
    if request.user.is_authenticated:
        if "venta" in request.session:
            for key, value in request.session["venta"].items():
                total += float(value.get("acumulado", 0))
    
    # Actualiza la variable de sesión con el nuevo total
    request.session["total_venta"] = total
    request.session.modified = True
    
    return {"total_venta": total}
