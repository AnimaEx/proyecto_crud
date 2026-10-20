from django.urls import path

from django.contrib.auth import views as auth_views


from .views import (
    registro,
    home,
    detalle_inmueble,
    perfil_usuario,
    editar_perfil,
    mis_inmuebles,
    publicar_inmueble,
    editar_inmueble,
    cambiar_estado_inmueble,
    solicitudes_usuario,
    editar_solicitud,
    eliminar_solicitud,
    administrar_horarios,
    eliminar_horario,
    marcar_notificacion_vista,
)


from .forms import LoginForm


app_name = 'gestion_inmuebles'


urlpatterns = [


    # ============================================================
    # HOME
    # ============================================================

    path(
        '',
        home,
        name='home'
    ),


    # ============================================================
    # LOGIN
    # ============================================================

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='login.html',
            authentication_form=LoginForm
        ),
        name='login'
    ),


    # ============================================================
    # LOGOUT
    # ============================================================

    path(
        'logout/',
        auth_views.LogoutView.as_view(
            template_name='logout.html'
        ),
        name='logout'
    ),


    # ============================================================
    # REGISTRO
    # ============================================================

    path(
        'register/',
        registro,
        name='register'
    ),


    # ============================================================
    # PUBLICAR INMUEBLE
    # ============================================================

    path(
        'inmueble/publicar/',
        publicar_inmueble,
        name='publicar_inmueble'
    ),


    # ============================================================
    # EDITAR INMUEBLE
    # ============================================================

    path(
        'inmueble/<int:inmueble_id>/editar/',
        editar_inmueble,
        name='editar_inmueble'
    ),


    # ============================================================
    # PUBLICAR / OCULTAR INMUEBLE
    # ============================================================

    path(
        'inmueble/<int:inmueble_id>/estado/',
        cambiar_estado_inmueble,
        name='cambiar_estado_inmueble'
    ),


    # ============================================================
    # DETALLE DE INMUEBLE
    # ============================================================

    path(
        'inmueble/<int:inmueble_id>/',
        detalle_inmueble,
        name='detalle_inmueble'
    ),


    # ============================================================
    # PERFIL
    # ============================================================

    path(
        'perfil/',
        perfil_usuario,
        name='perfil'
    ),


    # ============================================================
    # EDITAR PERFIL
    # ============================================================

    path(
        'perfil/editar/',
        editar_perfil,
        name='editar_perfil'
    ),
    
    # ============================================================
    # MIS INMUEBLES
    # ============================================================

    path(
        'mis-inmuebles/',
        mis_inmuebles,
        name='mis_inmuebles'
    ),


    # ============================================================
    # SOLICITUDES
    # ============================================================

    path(
        'solicitudes/',
        solicitudes_usuario,
        name='solicitudes'
    ),


    # ============================================================
    # EDITAR SOLICITUD
    # ============================================================

    path(
        'solicitud/<int:solicitud_id>/editar/',
        editar_solicitud,
        name='editar_solicitud'
    ),


    # ============================================================
    # ELIMINAR SOLICITUD
    # ============================================================

    path(
        'solicitud/<int:solicitud_id>/eliminar/',
        eliminar_solicitud,
        name='eliminar_solicitud'
    ),


    # ============================================================
    # ADMINISTRAR HORARIOS
    # ============================================================

    path(
        'inmueble/<int:inmueble_id>/horarios/',
        administrar_horarios,
        name='administrar_horarios'
    ),


    # ============================================================
    # ELIMINAR HORARIO
    # ============================================================

    path(
        'horario/<int:horario_id>/eliminar/',
        eliminar_horario,
        name='eliminar_horario'
    ),

    path(
    'solicitud/<int:solicitud_id>/notificacion/<str:tipo>/',
    marcar_notificacion_vista,
    name='marcar_notificacion_vista'
    ),
    
]