from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
from aplicacionGeneral.carrito import Carrito
from aplicacionGeneral.context_processor import total_carrito
from aplicacionGeneral.forms import PersonaForm, RegistroUsuarioForm, PedidoForm
from aplicacionGeneral.models import *
#Formulario para el LOGIN
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,logout,authenticate

# Create your views here.

def inicio(request):
    # Se recupera la cantidad de registros de la tabla servicios
    numero_servicios_var = Servicio.objects.count()
    # Recupera todos los servicios ordenados por id
    servicios_var = Servicio.objects.order_by('id')

    #Se llama a la página que presentará los servicios y se le envian los dos parámetros
    #calculados anteriormente para que los pueda manipular
    return render(request, "tienda.html", {'numero_servicios_var': numero_servicios_var,
                                           'todos_servicios_var': servicios_var})

def ver_pedidos(request):

    #Se recupera el cliente que está conectado en una variable
    cliente_actual = request.user

    # Se recupera las ordenes del cliente conectado. Se utiliza filter si se recupera más de una
    lista_pedidos_cliente = Ordenes.objects.filter(cliente = cliente_actual)

    #Se llama a la página que presentará los pedidos y se le envian los dos parámetros
    #calculados anteriormente para que los pueda manipular
    return render(request, "ver_pedidos.html", {'lista_pedidos_cliente': lista_pedidos_cliente})

def ver_detalle(request, pedido_id):

    # Se recupera las ordenes del cliente conectado. Se utiliza filter si se recupera más de una
    lista_servicios_pedido = Ordenes_Items.objects.filter(orden = pedido_id)

    #Se llama a la página que presentará los pedidos y se le envian los dos parámetros
    #calculados anteriormente para que los pueda manipular
    return render(request, "ver_detalle.html", {'lista_servicios_pedido': lista_servicios_pedido,
                                                'pedido_id': pedido_id})


def agregar_producto(request, servicio_id):
    #Se crea un objeto de la clase Carrito que llama a su constructor __init__
    carrito = Carrito(request)
    # Se obtiene la identificación del servicio actual
    servicio = Servicio.objects.get(id=servicio_id)
    # Se llama al método agregar del objeto carrito con la identificación del servicio
    carrito.agregar(servicio)
    return redirect('inicio')

def eliminar_producto (request, servicio_id):
    carrito = Carrito(request)
    servicio = Servicio.objects.get(id=servicio_id)
    carrito.eliminar_carrito(servicio)
    return redirect('inicio')

def restar_producto(request, servicio_id):
    carrito = Carrito(request)
    servicio = Servicio.objects.get(id=servicio_id)
    carrito.restar(servicio)
    return redirect('inicio')

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect('inicio')


def registro(request):

    if request.method == 'POST': # Si los campos están rellenos
        formularioCreacion = RegistroUsuarioForm(request.POST) #Se almacena la información del formulario
        if formularioCreacion.is_valid(): #El formulario se ha rellenado correctamente
            formularioCreacion.save()     #Se guardan los datos en el tabla.
            #username = formularioCreacion.cleaned_data['username']
            #messages.success(request, f'Usuario {username} creado correctamente')
            #messages.success(request,f'Usario creado correctamente')
            return redirect('inicio')
        else:
            return render(request, 'registro.html', {'formularioCreacion' : formularioCreacion})
    else:
        formularioCreacion = RegistroUsuarioForm() # Si los campos están vacíos no hacer nada
        return render(request, 'registro.html', {'formularioCreacion': formularioCreacion})

def logout_request(request):
    logout(request)
    messages.info(request, "Saliste con éxito")
    #return redirect("salir")
    return render(request, 'logout.html')
    #return HttpResponse ("Saliste con éxito")

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            usuario     = form.cleaned_data.get('username')
            contraseña  = form.cleaned_data.get('password')
            user = authenticate(username=usuario, password=contraseña)

            if user is not None:
                login(request,user) # Está relacionado con la variable LOGIN_REDIRECT_URL = 'inicio'
                messages.info(request, f"Ha ingresado el usuario: {usuario}") #no sale
                #return HttpResponse ("You are LOG IN")
                return redirect("inicio")
            else:
                messages.error(request, "Usuario o contraseña equivocada") #no sale
        else:
            messages.error(request, "Usuario o contraseña equivocada") #no sale

    form = AuthenticationForm()
    return render(request, 'login.html', {"form": form})

#Solicta login antes de entrar a esta función
@login_required(login_url='login')
def hacer_pedido(request):

    if request.method == "POST":
        total = 0
        # Se valida si hay elementos en el carrito para calcular el precio total de los elementos
        if "carrito" in request.session.keys():
            for key, value in request.session["carrito"].items():
                total += int(value["acumulado"])

        #Se crea una variable con el formato de la tabla de ordenes
        nuevaOrden=Ordenes()

        #Inserta la dirección del formulario
        nuevaOrden.direccion = request.POST.get('direccion')
        nuevaOrden.telefono = request.POST.get('telefono')

        #Se recupera el cliente que está conectado en una variable
        nuevaOrden.cliente = request.user
        nuevaOrden.precio_total = total
        nuevaOrden.save()

        #Se guardan cada unos de los items del carrito en la tabla de Ordenes_Item
        if "carrito" in request.session.keys():
            for key, value in request.session["carrito"].items():
                nuevoItem = Ordenes_Items()
                nuevoItem.orden = Ordenes.objects.get(id=nuevaOrden.id)
                nuevoItem.servicio = Servicio.objects.get(id=int(value["producto_id"]))
                nuevoItem.cantidad = int(value["cantidad"])
                nuevoItem.precio_serv = int(value["acumulado"])
                nuevoItem.save()

        #return HttpResponse("Se ha guardado la orden")
        return render(request, 'guardar_pedido.html')

    else:
        formularioPedido = PedidoForm(request.POST)  # Si los campos están vacíos no hacer nada
        return render(request, 'hacer_pedido.html', {'formularioPedido': formularioPedido})