#Permite guardar de forma global el total de la compra

def total_carrito(request):
    total = 0
    #if request.user.is_authenticated:
    if "carrito" in request.session.keys():
        for key, value in request.session["carrito"].items():
            total += int(value["acumulado"])
                #total += 1
    return {"total_carrito": total}
