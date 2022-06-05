class Carrito:
    def __init__(self, request):

        #Se obtienen todos los datos o variables de sesión con el parámetro request, atributo session.
        self.request = request
        self.session = request.session

        # Se obtiene específicamente la variable carrito de lso datos de sesión.
        carrito = self.session.get("carrito")

        # Si la variable carrito no existe en la sesión, se crea dicha variable en la sesión.
          #- Se crea la variable dentros de la sesión y se inicializa
          # Se le asigna la variabla de sesión (session["carrito"]) a una variable local (carrito).

        # Si la variable carrito si existe en la sesión (session["carrito"]),
        # se le asigna a una varibale local (carrito)

        if not carrito:
            self.session["carrito"] = {}
            self.carrito = self.session["carrito"]
        else:
            self.carrito = carrito

    # Se usa la funcion keys para revisar los indices de la variable sesión.
    # Se revisa que el índice haya que haa llegado (id del servicio), se encuentre en la variable
    # de sesión. En esta caso la variable de sesión es diccionario de datos (id: producto_id, nombre,
    # acumulado, cantidad)
    # Si el servicio (producto.id) no está en el carrito crea un nuevo registro.
    # Si el servicio (producto.id) si está en el carrito acumula la cantidad y
    # el precio en el servicio que ha llegado.

    def agregar(self, producto):
        id = str(producto.id)
        if id not in self.carrito.keys():
            self.carrito[id]={
                "producto_id": producto.id,
                "nombre": producto.servicio,
                "acumulado": producto.precio,
                "cantidad": 1,
            }
        else:
            self.carrito[id]["cantidad"] += 1
            self.carrito[id]["acumulado"] += producto.precio
        self.guardar_carrito()

    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def eliminar(self, servicio):
        id = str(servicio.id)
        if id in self.carrito:
            del self.carrito[id]
            self.guardar_carrito()

    def restar(self, servicio):
        id = str(servicio.id)
        if id in self.carrito.keys():
            self.carrito[id]["cantidad"] -= 1
            self.carrito[id]["acumulado"] -= servicio.precio
            if self.carrito[id]["cantidad"] <= 0: self.eliminar(servicio)
            self.guardar_carrito()

    def limpiar (self):
        #self.carrito["carrito"] = {}
        self.session["carrito"] = {}
        self.session.modified = True