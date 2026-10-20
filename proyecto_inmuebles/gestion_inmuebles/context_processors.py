# ============================================================
# NOTIFICACIONES DEL NAVBAR
# ============================================================

from .models import PerfilUsuario, SolicitudArriendo


def notificaciones_navbar(request):


    # Por defecto no hay notificaciones
    total_visitas_nuevas = 0


    # ============================================================
    # USUARIO AUTENTICADO
    # ============================================================

    if request.user.is_authenticated:


        perfil = PerfilUsuario.objects.filter(
            user=request.user
        ).first()


        # ========================================================
        # SOLO ARRENDADOR
        # ========================================================

        if (
            perfil
            and perfil.tipo_usuario == 'arrendador'
        ):


            # ====================================================
            # RESERVAS NUEVAS
            # ====================================================

            reservas_nuevas = SolicitudArriendo.objects.filter(

                inmueble__arrendador=perfil,

                estado='reservada',

                vista_arrendador=False

            ).count()


            # ====================================================
            # CANCELACIONES NUEVAS
            # ====================================================

            cancelaciones_nuevas = SolicitudArriendo.objects.filter(

                inmueble__arrendador=perfil,

                estado='cancelada',

                cancelacion_vista_arrendador=False

            ).count()


            # ====================================================
            # TOTAL
            # ====================================================

            total_visitas_nuevas = (
                reservas_nuevas
                +
                cancelaciones_nuevas
            )


    return {

        'total_visitas_nuevas': total_visitas_nuevas

    }