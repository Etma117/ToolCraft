from decimal import Decimal

def total_venta(request):
    total = 0
    if request.user.is_authenticated:
        if "venta" in request.session.keys():
            for key, value in request.session["venta"].items():
                total += float(value["acumulado"])
                print(total)
    return {"total_venta": Decimal(total)}
