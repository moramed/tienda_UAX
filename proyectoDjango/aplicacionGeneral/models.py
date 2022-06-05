import datetime

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Servicio (models.Model):
    servicio = models.CharField(max_length=255)
    detalle  = models.CharField(max_length=255)
    precio   = models.IntegerField()

    def __str_(self):
        return f'Producto {self.id}: {self.servicio} {self.detalle} {self.precio}'

class Persona(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    usuario = models.CharField(max_length=8)
    clave = models.CharField(max_length=4)

    # Método para mostrar la información concatenada.

    def __str__(self):
        return f'Persona {self.id}: {self.nombre} {self.email} {self.usuario}'

class Ordenes(models.Model):
    #Diccionario de datos para el estado
    STATUS = (
        ('New','Nuevo'), #Etiqueta + valor
        ('Accepted','Aceptado'),
        ('Ongoing','En curso'),
        ('Completed','Finalizado'),
        ('Cancelled','Cancelado'),
    )

    cliente      = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    precio_total = models.IntegerField(default=0)
    direccion    = models.CharField(max_length=50, default='', blank=True)
    telefono     = models.CharField(max_length=50, default='', blank=True)
    fecha        = models.DateTimeField(auto_now_add=True)
    estado_orden = models.CharField(max_length=50, choices=STATUS, default='New')

    def __str__(self):
        return f'Ordenes {self.id}: {self.cliente} {self.precio_total} {self.fecha} {self.estado_orden}'


class Ordenes_Items(models.Model):
    orden        = models.ForeignKey(Ordenes,on_delete=models.CASCADE, null=True)
    servicio     = models.ForeignKey(Servicio, on_delete=models.CASCADE, blank=True, null=True)
    cantidad     = models.IntegerField(default=0)
    precio_serv  = models.IntegerField(default=0)

    def __str__(self):
        return f'Ordenes_Items {self.orden}: {self.servicio} {self.cantidad} {self.precio_serv}'
