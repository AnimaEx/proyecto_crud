

# Register your models here.
from django.contrib import admin
from .models import Region, Comuna, PerfilUsuario, Inmueble, SolicitudArriendo,TipoInmueble

# Register your models here.
#admin.site.register(Region)
#admin.site.register(Comuna)
admin.site.register(PerfilUsuario)
admin.site.register(TipoInmueble)
#admin.site.register(Inmueble)
admin.site.register(SolicitudArriendo)

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)


@admin.register(Comuna)
class ComunaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'region')
    search_fields = ('nombre',)
    list_filter = ('region',)

@admin.register(Inmueble)
class InmuebleAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'direccion',
        'precio_mensual',
        'comuna',
        'tipo_inmueble',
        'arrendador',
    )

    search_fields = (
        'nombre',
        'direccion',
    )

    list_filter = (
        'comuna',
        'tipo_inmueble',
    )