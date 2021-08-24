from django.contrib import admin
from django.utils.safestring import mark_safe
from easy_select2 import select2_modelform


# Register your models here.
from .models import Distrito
from .models import Olt
from .models import TarjetaOLT
from .models import Distribucion_Puertos_a_Distrito
from .models import VLAN
from .models import IP_Address
from .models import Red_Alimentacion
from .models import Hilos_Alimentacion
from .models import Red_Distribucion
from .models import NAP
from .models import Plan_Contratado
from .models import Cliente 

from .forms import NAPFormAdmin


class ClienteAdmin(admin.ModelAdmin):
	readonly_fields=("IP", "Script")
	ordering = ('Distrito','Nap')
	search_fields = ('Nombre',)
	list_filter = ('Distrito','Nap')
	list_display = ('Nombre','Sn_auth', 'Plan_Contratado', 'Distrito', 'Nap', 'IP')
    
class DistritoAdmin(admin.ModelAdmin):
    list_display = ('Nombre','Descripcion')
    list_filter = ('Nombre','Descripcion')
    ordering = ('-Nombre',)
    search_fields = ('Nombre',)

class OltAdmin(admin.ModelAdmin):
    list_display = ('Detalle','Modelo', 'Capacidad')
    list_filter = ('MAC_OLT',)
    ordering = ('MAC_OLT',)
    search_fields = ('Detalle',)

class Plan_ContratadoAdmin(admin.ModelAdmin):
    list_display = ('Velocidad', 'Detalle')
    list_filter = ('Velocidad',)
    ordering = ('Velocidad',)
    search_fields = ('Velocidad',)

class Distribucion_Puertos_a_DistritoAdmin(admin.ModelAdmin):
    list_display = ('Numero_Puerto','Descripcion', 'Tarjeta','VLAN')
    list_filter = ('Numero_Puerto','Tarjeta','VLAN')
    ordering = ('Numero_Puerto',)
    search_fields = ('Numero_Puerto',)

class VLANAdmin(admin.ModelAdmin):
    list_display = ('ID','Numero','Detalle','Gemport','ServicePort','LineProfile','UserVlan')
    ordering = ('ID',)
    search_fields = ('ID',)

class TarjetaOLTAdmin(admin.ModelAdmin):
    list_display = ('Numero_Tarjeta','Capacidad', 'Olt')
    list_filter = ('Olt','Capacidad')
    ordering = ('Numero_Tarjeta',)
    search_fields = ('Olt',)

class IP_AddressAdmin(admin.ModelAdmin):
    list_filter = ('Vlan',)
    search_fields = ('IP',)
    list_display=('ip','Vlan')
    
class NAPAdmin(admin.ModelAdmin):
    form = NAPFormAdmin
    list_display = ('Codigo','Hilo', 'Tubillo','Capacidad','Ubicacion','FO_Distribucion','Spliiter_principal', "disponible")
    list_filter = ('FO_Distribucion','Spliiter_principal')
    ordering = ('Codigo',)
    search_fields = ('Codigo',)

    def disponible(self, obj):
        color = "green"
        disponible_valor = obj.avilables()
        if disponible_valor <= 4:
            color = "red"
        elif disponible_valor <= 8:
            color = "yellow"

        returned =  f'<div style="width:100%; height:100%; background-color:{color}; text-align: center; color: black; font-weight: bold;">{disponible_valor}</div>' 
        return mark_safe(returned)

class Red_DistribucionAdmin(admin.ModelAdmin):
	ordering = ('ID_FO',)
	list_filter = ('Distrito',)
	search_fields = ('Distrito',)
	list_display = ('ID_FO','Detalle_recorrido', 'Capacidad','Marca','Distrito')
    
class Red_AlimentacionAdmin(admin.ModelAdmin):
	ordering = ('ID_FO',)
	list_filter = ('Capacidad',)
	search_fields = ('Detalle_recorrido',)
	list_display = ('ID_FO','Detalle_recorrido', 'Capacidad','Marca')

class Hilos_AlimentacionAdmin(admin.ModelAdmin):
	ordering = ('Tubillo',)
	list_filter = ('FO_Alimentacion', 'puertos')
	search_fields = ('Color_hilo', 'puertos')
	list_display = ('Tubillo', 'Color_hilo','FO_Alimentacion', "estado")
    
admin.site.register(Olt,OltAdmin)
admin.site.register(TarjetaOLT,TarjetaOLTAdmin)
admin.site.register(Distrito, DistritoAdmin)
admin.site.register(VLAN,VLANAdmin)
admin.site.register(Distribucion_Puertos_a_Distrito, Distribucion_Puertos_a_DistritoAdmin)
admin.site.register(IP_Address,IP_AddressAdmin)
admin.site.register(Red_Alimentacion,Red_AlimentacionAdmin)
admin.site.register(Hilos_Alimentacion,Hilos_AlimentacionAdmin)
admin.site.register(Red_Distribucion, Red_DistribucionAdmin)
admin.site.register(NAP, NAPAdmin)
admin.site.register(Plan_Contratado,Plan_ContratadoAdmin)
admin.site.register(Cliente, ClienteAdmin)



