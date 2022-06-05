from django.contrib import admin
from django.contrib.auth.models import Group


# Register your models here.
from aplicacionGeneral.models import Servicio, Ordenes, Ordenes_Items

admin.site.register(Servicio)
admin.site.register(Ordenes)
admin.site.register(Ordenes_Items)
#Remove groups
admin.site.unregister(Group)

