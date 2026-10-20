from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import transaction
from datetime import date
from django.utils import timezone
from .models import (Inmueble, PerfilUsuario,TipoInmueble,Region,Comuna,SolicitudArriendo,HorarioVisita,)
from .forms import (RegistroForm,EditarUsuarioForm,EditarPerfilForm,EditarSolicitudForm,ReservaVisitaForm,HorarioVisitaForm,InmuebleForm,)


# ============================================================

# CRUD INMUEBLES

# ============================================================


def crea_inmueble(datos):
    id_propietario = datos['id_propietario']
    nombre = datos['nombre']
    descripcion = datos['descripcion']
    m2_construidos = datos['m2_construidos']
    m2_totales = datos['m2_totales']
    estacionamientos = datos['estacionamientos']
    habitaciones = datos['habitaciones']
    banos = datos['banos']
    direccion = datos['direccion']
    id_comuna = datos['id_comuna']
    id_tipo_inmueble = datos['id_tipo_inmueble']
    precio_mensual = datos['precio_mensual']
    inmueble = Inmueble.objects.create(
        nombre=nombre,
        descripcion=descripcion,
        m2_construidos=m2_construidos,
        m2_totales=m2_totales,
        estacionamientos=estacionamientos,
        habitaciones=habitaciones,
        banos=banos,
        direccion=direccion,
        comuna_id=id_comuna,
        tipo_inmueble_id=id_tipo_inmueble,
        precio_mensual=precio_mensual,
        arrendador_id=id_propietario
    )

    return inmueble

def listar_inmueble():
    inmuebles = Inmueble.objects.all()
    return inmuebles

def actualiza_inmueble(id_inmueble, datos):
    inmueble = Inmueble.objects.get(
        id=id_inmueble
    )
    inmueble.nombre = datos['nombre']
    inmueble.descripcion = datos['descripcion']
    inmueble.m2_construidos = datos['m2_construidos']
    inmueble.m2_totales = datos['m2_totales']
    inmueble.estacionamientos = datos['estacionamientos']
    inmueble.habitaciones = datos['habitaciones']
    inmueble.banos = datos['banos']
    inmueble.direccion = datos['direccion']
    inmueble.comuna_id = datos['id_comuna']
    inmueble.tipo_inmueble_id = datos['id_tipo_inmueble']
    inmueble.precio_mensual = datos['precio_mensual']
    inmueble.arrendador_id = datos['id_propietario']
    inmueble.save()

    return inmueble

def borrar_inmueble(id_inmueble):
    inmueble = Inmueble.objects.get(

        id=id_inmueble

    )

    inmueble.delete()

    return True


# ============================================================

# CRUD USUARIOS

# ============================================================


def crea_usuario(datos):
    username = datos['username']
    password = datos['password']
    nombres = datos['nombres']
    apellidos = datos['apellidos']
    correo = datos['correo']
    rut = datos['rut']
    direccion = datos['direccion']
    telefono = datos['telefono']
    tipo_usuario = datos['tipo_usuario']

    usuario = User.objects.create_user(
        username=username,
        password=password,
        first_name=nombres,
        last_name=apellidos,
        email=correo
    )

    PerfilUsuario.objects.create(
        user=usuario,
        rut=rut,
        direccion=direccion,
        telefono=telefono,
        tipo_usuario=tipo_usuario
    )

    return usuario

def listar_usuarios():
    usuarios = PerfilUsuario.objects.all()
    return usuarios

def actualiza_usuario(id_usuario, datos):

    usuario = User.objects.get(

        id=id_usuario
    )

    perfil = PerfilUsuario.objects.get(

        user=usuario

    )

    usuario.username = datos['username']
    usuario.first_name = datos['nombres']
    usuario.last_name = datos['apellidos']
    usuario.email = datos['correo']
    perfil.rut = datos['rut']
    perfil.direccion = datos['direccion']
    perfil.telefono = datos['telefono']
    perfil.tipo_usuario = datos['tipo_usuario']

    usuario.save()
    perfil.save()
    return usuario

def borrar_usuario(id_usuario):

    usuario = User.objects.get(

        id=id_usuario

    )

    usuario.delete()

    return True


# ============================================================

# REGISTRO

# ============================================================


def registro(request):

    if request.method == 'POST':

        form = RegistroForm(

            request.POST

        )

        if form.is_valid():

            form.save()

            return redirect(

                'gestion_inmuebles:login'

            )

    else:

        form = RegistroForm()

    return render(

        request,

        'register.html',

        {

            'form': form

        }

    )

# ============================================================

# HOME

# ============================================================

def home(request):

    inmuebles = Inmueble.objects.filter(

    publicado=True

    )

    tipo = request.GET.get(

        'tipo'

    )

    region = request.GET.get(

        'region'

    )

    comuna = request.GET.get(

        'comuna'

    )


    # ============================================================

    # FILTROS

    # ============================================================


    if tipo:


        inmuebles = inmuebles.filter(

            tipo_inmueble_id=tipo

        )


    if region:


        inmuebles = inmuebles.filter(

            comuna__region_id=region

        )


    if comuna:


        inmuebles = inmuebles.filter(

            comuna_id=comuna

        )


    tipos = TipoInmueble.objects.all()


    regiones = Region.objects.all()


    comunas = Comuna.objects.all()


    # ============================================================

    # INMUEBLES DONDE EL USUARIO YA ENVIÓ SOLICITUD

    # ============================================================


    inmuebles_solicitados = []


    if request.user.is_authenticated:


        perfil = PerfilUsuario.objects.filter(

            user=request.user

        ).first()


        if (

            perfil

            and perfil.tipo_usuario == 'arrendatario'

        ):


            inmuebles_solicitados = list(


                SolicitudArriendo.objects.filter(

                    arrendatario=perfil,

                    estado='reservada'

                ).values_list(

                    'inmueble_id',

                    flat=True

                )


            )


    # ============================================================

    # INMUEBLES YA VISTOS

    # ============================================================


    inmuebles_vistos = request.session.get(

        'inmuebles_vistos',

        []

    )


    # ============================================================

    # CONTEXTO

    # ============================================================


    context = {


        'inmuebles': inmuebles,


        'tipos': tipos,


        'regiones': regiones,


        'comunas': comunas,


        'tipo_seleccionado': tipo,


        'region_seleccionada': region,


        'comuna_seleccionada': comuna,


        'inmuebles_solicitados': inmuebles_solicitados,


        'inmuebles_vistos': inmuebles_vistos,


    }


    return render(

        request,

        'home.html',

        context

    )

# ============================================================

# DETALLE DEL INMUEBLE

# ============================================================

def detalle_inmueble(request, inmueble_id):


    # ============================================================

    # BUSCAR INMUEBLE

    # ============================================================


    inmueble = get_object_or_404(

        Inmueble,

        id=inmueble_id

    )


    # ============================================================

    # GUARDAR INMUEBLE COMO VISTO

    # ============================================================


    inmuebles_vistos = request.session.get(

        'inmuebles_vistos',

        []

    )

    if inmueble.id not in inmuebles_vistos:

        inmuebles_vistos.append(

            inmueble.id

        )

        request.session[

            'inmuebles_vistos'

        ] = inmuebles_vistos

    # ============================================================

    # DATOS INICIALES

    # ============================================================


    perfil = None
    solicitud_existente = None

    # ============================================================

    # HORARIOS DISPONIBLES

    # ============================================================

    horarios_disponibles = HorarioVisita.objects.filter(

        inmueble=inmueble,

        disponible=True,

        fecha__gte=date.today()

    ).order_by(

        'fecha',

        'hora'
    )


    # ============================================================

    # USUARIO AUTENTICADO

    # ============================================================


    if request.user.is_authenticated:

        perfil = PerfilUsuario.objects.filter(

            user=request.user

        ).first()

        if (

            perfil

            and perfil.tipo_usuario == 'arrendatario'

        ):

            solicitud_existente = (

                SolicitudArriendo.objects.filter(

                    arrendatario=perfil,

                    inmueble=inmueble,
                    
                    estado='reservada'

                ).first()

            )


    # ============================================================

    # FORMULARIO DE RESERVA

    # ============================================================


    form_reserva = ReservaVisitaForm(

        inmueble=inmueble

    )


    # ============================================================

    # RESERVAR VISITA

    # ============================================================


    if request.method == 'POST':


        # --------------------------------------------------------

        # DEBE TENER SESIÓN INICIADA

        # --------------------------------------------------------

        if not request.user.is_authenticated:

            return redirect(

                'gestion_inmuebles:login'

            )

        # --------------------------------------------------------

        # DEBE TENER PERFIL

        # --------------------------------------------------------

        if perfil is None:

            return redirect(

                'gestion_inmuebles:detalle_inmueble',

                inmueble_id=inmueble.id

            )

        # --------------------------------------------------------

        # SOLO ARRENDATARIOS PUEDEN RESERVAR

        # --------------------------------------------------------

        if perfil.tipo_usuario != 'arrendatario':

            return redirect(

                'gestion_inmuebles:detalle_inmueble',

                inmueble_id=inmueble.id

            )

        # --------------------------------------------------------

        # NO PUEDE RESERVAR DOS VECES EL MISMO INMUEBLE

        # --------------------------------------------------------

        if solicitud_existente:

            return redirect(

                'gestion_inmuebles:detalle_inmueble',

                inmueble_id=inmueble.id

            )

        # --------------------------------------------------------

        # FORMULARIO

        # --------------------------------------------------------

        form_reserva = ReservaVisitaForm(

            request.POST,
            inmueble=inmueble

        )

        if form_reserva.is_valid():

            horario_form = (

                form_reserva.cleaned_data[

                    'horario'

                ]

            )

            # ====================================================

            # TRANSACCIÓN

            # ====================================================

            with transaction.atomic():


                # ------------------------------------------------

                # BLOQUEAMOS EL HORARIO

                # ------------------------------------------------

                horario = get_object_or_404(

                    HorarioVisita.objects.select_for_update(),

                    id=horario_form.id,
                    inmueble=inmueble,
                    disponible=True

                )


                # ------------------------------------------------

                # CREAMOS LA SOLICITUD

                # ------------------------------------------------

                solicitud = form_reserva.save(

                    commit=False

                )

                solicitud.arrendatario = perfil
                solicitud.inmueble = inmueble
                solicitud.horario = horario

                # ------------------------------------------------

                # COPIAMOS FECHA Y HORA

                # ------------------------------------------------

                solicitud.fecha_visita = (
                    horario.fecha
                )

                solicitud.hora_visita = (
                    horario.hora
                )

                # ------------------------------------------------

                # LA VISITA QUEDA CONFIRMADA

                # ------------------------------------------------

                solicitud.aceptada = True
                solicitud.save()

                # ------------------------------------------------

                # EL HORARIO YA NO ESTÁ DISPONIBLE

                # ------------------------------------------------

                horario.disponible = False
                horario.save()

            return redirect(

                'gestion_inmuebles:solicitudes'

            )

    # ============================================================

    # CONTEXTO

    # ============================================================

    context = {

        'inmueble': inmueble,
        'perfil': perfil,
        'solicitud_existente': solicitud_existente,
        'horarios_disponibles': horarios_disponibles,
        'form_reserva': form_reserva,

    }

    return render(

        request,

        'detalle_inmueble.html',

        context

    )

# ============================================================

# PERFIL

# ============================================================

@login_required
def perfil_usuario(request):
    perfil = get_object_or_404(
        PerfilUsuario,
        user=request.user
    )

    return render(
        request,
        'perfil.html',
        {
            'perfil': perfil
        }
    )

# ============================================================
# MIS INMUEBLES
# ============================================================

@login_required
def mis_inmuebles(request):
    perfil = get_object_or_404(
        PerfilUsuario,
        user=request.user,
        tipo_usuario='arrendador'
    )

    inmuebles = Inmueble.objects.filter(
        arrendador=perfil
    ).order_by(
        '-id'
    )

    return render(
        request,
        'mis_inmuebles.html',
        {
            'perfil': perfil,
            'inmuebles': inmuebles
        }
    )

# ============================================================

# EDITAR PERFIL

# ============================================================

@login_required
def editar_perfil(request):


    perfil = get_object_or_404(

        PerfilUsuario,

        user=request.user

    )


    if request.method == 'POST':


        form_usuario = EditarUsuarioForm(


            request.POST,


            instance=request.user


        )


        form_perfil = EditarPerfilForm(


            request.POST,


            instance=perfil


        )


        if (

            form_usuario.is_valid()

            and form_perfil.is_valid()

        ):


            form_usuario.save()


            form_perfil.save()


            return redirect(

                'gestion_inmuebles:perfil'

            )


    else:


        form_usuario = EditarUsuarioForm(

            instance=request.user

        )


        form_perfil = EditarPerfilForm(

            instance=perfil

        )


    context = {


        'perfil': perfil,


        'form_usuario': form_usuario,


        'form_perfil': form_perfil,


    }


    return render(

        request,

        'editar_perfil.html',

        context

    )

# ============================================================

# PUBLICAR INMUEBLE

# ============================================================

@login_required
def publicar_inmueble(request):


    # ============================================================

    # PERFIL DEL ARRENDADOR

    # ============================================================


    perfil = get_object_or_404(


        PerfilUsuario,


        user=request.user,


        tipo_usuario='arrendador'


    )


    # ============================================================

    # REGIONES Y COMUNAS

    # ============================================================


    regiones = Region.objects.all().order_by(

        'nombre'

    )


    comunas = Comuna.objects.all().order_by(

        'nombre'

    )


    # ============================================================

    # POST

    # ============================================================


    if request.method == 'POST':


        form = InmuebleForm(


            request.POST,


            request.FILES


        )


        if form.is_valid():


            inmueble = form.save(

                commit=False

            )


            inmueble.arrendador = perfil


            inmueble.save()


            return redirect(

                'gestion_inmuebles:mis_inmuebles'

            )


    # ============================================================

    # GET

    # ============================================================


    else:


        form = InmuebleForm()


    # ============================================================

    # CONTEXTO

    # ============================================================


    context = {


        'form': form,


        'perfil': perfil,


        'regiones': regiones,


        'comunas': comunas,


        'region_seleccionada': request.POST.get(

            'region',

            ''

        ),


        'comuna_seleccionada': request.POST.get(

            'comuna',

            ''

        ),


    }


    return render(


        request,


        'publicar_inmueble.html',


        context


    )

# ============================================================
# SOLICITUDES DEL USUARIO
# ============================================================

@login_required
def solicitudes_usuario(request):


    # ============================================================
    # PERFIL DEL USUARIO
    # ============================================================

    perfil = get_object_or_404(
        PerfilUsuario,
        user=request.user
    )


    # ============================================================
    # ORDEN SELECCIONADO
    # ============================================================

    orden = request.GET.get(
        'orden',
        'todas'
    )


    # ============================================================
    # LISTAS PARA NOTIFICACIONES DEL ARRENDADOR
    # ============================================================

    nuevas_solicitudes = SolicitudArriendo.objects.none()

    cancelaciones_nuevas = SolicitudArriendo.objects.none()


    # ============================================================
    # ARRENDATARIO
    # ============================================================

    if perfil.tipo_usuario == 'arrendatario':


        # Solo mostramos reservas activas al arrendatario.

        solicitudes = SolicitudArriendo.objects.filter(

            arrendatario=perfil,

            estado='reservada'

        ).select_related(

            'inmueble',
            'horario'

        ).order_by(

            'fecha_visita',
            'hora_visita'

        )


    # ============================================================
    # ARRENDADOR
    # ============================================================

    elif perfil.tipo_usuario == 'arrendador':


        # ========================================================
        # VISITAS ACTIVAS
        # ========================================================

        # La lista principal inferior muestra solamente
        # solicitudes que siguen reservadas.
        # Las canceladas se conservan en la base de datos,
        # pero no aparecen en esta lista.

        solicitudes = SolicitudArriendo.objects.filter(

            inmueble__arrendador=perfil,

            estado='reservada'

        ).select_related(

            'inmueble',
            'horario',
            'arrendatario',
            'arrendatario__user'

        )


        # ========================================================
        # NUEVAS RESERVAS
        # ========================================================

        nuevas_solicitudes = SolicitudArriendo.objects.filter(

            inmueble__arrendador=perfil,

            estado='reservada',

            vista_arrendador=False

        ).select_related(

            'inmueble',
            'arrendatario',
            'arrendatario__user'

        ).order_by(

            '-fecha_creacion'

        )


        # ========================================================
        # CANCELACIONES NUEVAS
        # ========================================================

        # Las cancelaciones solo aparecen arriba como
        # notificaciones mientras no hayan sido vistas.

        cancelaciones_nuevas = SolicitudArriendo.objects.filter(

            inmueble__arrendador=perfil,

            estado='cancelada',

            cancelacion_vista_arrendador=False

        ).select_related(

            'inmueble',
            'arrendatario',
            'arrendatario__user'

        ).order_by(

            '-fecha_cancelacion'

        )


        # ========================================================
        # ORDENAR VISITAS ACTIVAS
        # ========================================================

        if orden == 'visita':

            # Visita más cercana primero.
            # Si son el mismo día, se ordenan por hora.

            solicitudes = solicitudes.order_by(
                'fecha_visita',
                'hora_visita'
            )


        else:

            # Todas las reservas activas.
            # La reserva creada más recientemente aparece primero.

            solicitudes = solicitudes.order_by(
                '-fecha_creacion',
                '-id'
            )


    # ============================================================
    # OTRO TIPO DE USUARIO
    # ============================================================

    else:

        solicitudes = SolicitudArriendo.objects.none()


    # ============================================================
    # CONTEXTO
    # ============================================================

    context = {

        'perfil': perfil,

        'solicitudes': solicitudes,

        'orden_seleccionado': orden,

        'nuevas_solicitudes': nuevas_solicitudes,

        'cancelaciones_nuevas': cancelaciones_nuevas,

    }


    # ============================================================
    # RENDER
    # ============================================================

    return render(
        request,
        'solicitudes.html',
        context
    )

# ============================================================
# MARCAR NOTIFICACIÓN COMO VISTA
# ============================================================

@login_required
def marcar_notificacion_vista(request, solicitud_id, tipo):


    # ============================================================
    # PERFIL DEL ARRENDADOR
    # ============================================================

    perfil = get_object_or_404(

        PerfilUsuario,

        user=request.user,

        tipo_usuario='arrendador'

    )


    # ============================================================
    # SOLICITUD
    # ============================================================

    solicitud = get_object_or_404(

        SolicitudArriendo,

        id=solicitud_id,

        inmueble__arrendador=perfil

    )


    # ============================================================
    # SOLO POST
    # ============================================================

    if request.method == 'POST':


        # ========================================================
        # RESERVA NUEVA
        # ========================================================

        if tipo == 'reserva':

            solicitud.vista_arrendador = True

            solicitud.save(
                update_fields=[
                    'vista_arrendador'
                ]
            )


        # ========================================================
        # CANCELACIÓN NUEVA
        # ========================================================

        elif tipo == 'cancelacion':

            solicitud.cancelacion_vista_arrendador = True

            solicitud.save(
                update_fields=[
                    'cancelacion_vista_arrendador'
                ]
            )


    return redirect(
        'gestion_inmuebles:solicitudes'
    )

# ============================================================

# EDITAR / CAMBIAR HORARIO DE UNA SOLICITUD

# ============================================================

@login_required
def editar_solicitud(request, solicitud_id):


    perfil = get_object_or_404(

        PerfilUsuario,

        user=request.user

    )


    solicitud = get_object_or_404(


        SolicitudArriendo,


        id=solicitud_id,


        arrendatario=perfil,
        
        estado='reservada'


    )


    if request.method == 'POST':


        form = EditarSolicitudForm(


            request.POST,


            instance=solicitud,


            inmueble=solicitud.inmueble


        )


        if form.is_valid():


            nuevo_horario_form = (

                form.cleaned_data[

                    'horario'

                ]

            )


            with transaction.atomic():


                solicitud = (


                    SolicitudArriendo.objects


                    .select_for_update()


                    .get(

                        id=solicitud.id

                    )


                )


                horario_anterior = (

                    solicitud.horario

                )


                # ====================================================

                # SI CAMBIÓ DE HORARIO

                # ====================================================


                if (


                    horario_anterior is None


                    or nuevo_horario_form.id

                    != horario_anterior.id


                ):


                    nuevo_horario = get_object_or_404(


                        HorarioVisita.objects.select_for_update(),


                        id=nuevo_horario_form.id,


                        inmueble=solicitud.inmueble,


                        disponible=True


                    )


                    # LIBERAR HORARIO ANTERIOR

                    if horario_anterior:


                        horario_anterior.disponible = True


                        horario_anterior.save()


                    # OCUPAR HORARIO NUEVO

                    nuevo_horario.disponible = False


                    nuevo_horario.save()


                    solicitud.horario = nuevo_horario


                    solicitud.fecha_visita = (

                        nuevo_horario.fecha

                    )


                    solicitud.hora_visita = (

                        nuevo_horario.hora

                    )


                solicitud.comentarios = (

                    form.cleaned_data[

                        'comentarios'

                    ]

                )


                solicitud.aceptada = True


                solicitud.save()


            return redirect(

                'gestion_inmuebles:solicitudes'

            )


    return redirect(

        'gestion_inmuebles:solicitudes'

    )

# ============================================================
# CANCELAR SOLICITUD
# ============================================================

@login_required
def eliminar_solicitud(request, solicitud_id):


    # ============================================================
    # PERFIL DEL ARRENDATARIO
    # ============================================================

    perfil = get_object_or_404(
        PerfilUsuario,
        user=request.user,
        tipo_usuario='arrendatario'
    )


    # ============================================================
    # SOLO ACEPTAMOS POST
    # ============================================================

    if request.method == 'POST':


        with transaction.atomic():


            # ====================================================
            # BUSCAR Y BLOQUEAR SOLICITUD
            # ====================================================

            solicitud = get_object_or_404(

                SolicitudArriendo.objects.select_for_update(),

                id=solicitud_id,

                arrendatario=perfil,

                estado='reservada'

            )


            # ====================================================
            # HORARIO RESERVADO
            # ====================================================

            horario = solicitud.horario


            # ====================================================
            # LIBERAR HORARIO
            # ====================================================

            if horario:

                horario.disponible = True

                horario.save(
                    update_fields=['disponible']
                )


            # ====================================================
            # CANCELAR SOLICITUD
            # ====================================================

            solicitud.estado = 'cancelada'

            solicitud.fecha_cancelacion = timezone.now()


            # Ya no dejamos el horario conectado a la solicitud
            # porque ese horario ahora puede ser reservado
            # nuevamente por otro arrendatario.

            solicitud.horario = None


            # ====================================================
            # NOTIFICACIÓN PARA EL ARRENDADOR
            # ====================================================

            # Si la reserva todavía aparecía como "nueva",
            # dejamos de contarla como nueva reserva.

            solicitud.vista_arrendador = True


            # Ahora debe aparecer como una nueva cancelación.

            solicitud.cancelacion_vista_arrendador = False


            # Campo antiguo que mantenemos por compatibilidad.

            solicitud.aceptada = False


            # ====================================================
            # GUARDAR SIN ELIMINAR
            # ====================================================

            solicitud.save(
                update_fields=[
                    'estado',
                    'fecha_cancelacion',
                    'horario',
                    'vista_arrendador',
                    'cancelacion_vista_arrendador',
                    'aceptada',
                ]
            )


        return redirect(
            'gestion_inmuebles:solicitudes'
        )


    return redirect(
        'gestion_inmuebles:solicitudes'
    )
        
# ============================================================

# ADMINISTRAR HORARIOS DEL INMUEBLE

# ============================================================

@login_required
def administrar_horarios(request, inmueble_id):


    # ============================================================

    # PERFIL DEL ARRENDADOR

    # ============================================================


    perfil = get_object_or_404(


        PerfilUsuario,


        user=request.user,


        tipo_usuario='arrendador'


    )


    # ============================================================

    # INMUEBLE

    # ============================================================


    inmueble = get_object_or_404(


        Inmueble,


        id=inmueble_id,


        arrendador=perfil


    )


    # ============================================================

    # AGREGAR HORARIO

    # ============================================================


    if request.method == 'POST':


        form = HorarioVisitaForm(

            request.POST

        )


        if form.is_valid():


            fecha = form.cleaned_data[

                'fecha'

            ]


            hora = form.cleaned_data[

                'hora'

            ]


            # ====================================================

            # EVITAR HORARIOS DUPLICADOS

            # ====================================================


            existe = HorarioVisita.objects.filter(


                inmueble=inmueble,


                fecha=fecha,


                hora=hora


            ).exists()


            if existe:


                form.add_error(


                    None,


                    'Este horario ya fue agregado.'


                )


            else:


                horario = form.save(

                    commit=False

                )


                horario.inmueble = inmueble


                horario.disponible = True


                horario.save()


                return redirect(


                    'gestion_inmuebles:administrar_horarios',


                    inmueble_id=inmueble.id


                )


    else:


        form = HorarioVisitaForm()


    # ============================================================

    # HORARIOS DEL INMUEBLE

    # ============================================================


    horarios = HorarioVisita.objects.filter(


        inmueble=inmueble


    ).order_by(


        'fecha',


        'hora'


    )


    context = {


        'perfil': perfil,


        'inmueble': inmueble,


        'horarios': horarios,


        'form': form,


    }


    return render(


        request,


        'administrar_horarios.html',


        context


    )

# ============================================================

# ELIMINAR HORARIO

# ============================================================

@login_required
def eliminar_horario(request, horario_id):


    perfil = get_object_or_404(


        PerfilUsuario,


        user=request.user,


        tipo_usuario='arrendador'


    )


    # ============================================================

    # HORARIO

    # ============================================================


    horario = get_object_or_404(


        HorarioVisita,


        id=horario_id,


        inmueble__arrendador=perfil,


        disponible=True


    )


    inmueble_id = (

        horario.inmueble.id

    )


    if request.method == 'POST':


        horario.delete()


    return redirect(


        'gestion_inmuebles:administrar_horarios',


        inmueble_id=inmueble_id


    )

# ============================================================

# EDITAR INMUEBLE

# ============================================================

@login_required
def editar_inmueble(request, inmueble_id):


    perfil = get_object_or_404(

        PerfilUsuario,

        user=request.user,

        tipo_usuario='arrendador'

    )


    inmueble = get_object_or_404(

        Inmueble,

        id=inmueble_id,

        arrendador=perfil

    )


    regiones = Region.objects.all().order_by(

        'nombre'

    )


    comunas = Comuna.objects.all().order_by(

        'nombre'

    )


    if request.method == 'POST':


        form = InmuebleForm(

            request.POST,

            request.FILES,

            instance=inmueble

        )


        if form.is_valid():


            form.save()


            return redirect(

                'gestion_inmuebles:mis_inmuebles'

            )


    else:


        form = InmuebleForm(

            instance=inmueble

        )


    context = {


        'form': form,


        'inmueble': inmueble,


        'regiones': regiones,


        'comunas': comunas,


        'region_seleccionada': str(

            inmueble.comuna.region_id

        ),


        'comuna_seleccionada': str(

            inmueble.comuna_id

        ),


    }


    return render(

        request,

        'editar_inmueble.html',

        context

    )

# ============================================================

# PUBLICAR / OCULTAR INMUEBLE

# ============================================================

@login_required
def cambiar_estado_inmueble(request, inmueble_id):


    perfil = get_object_or_404(

        PerfilUsuario,

        user=request.user,

        tipo_usuario='arrendador'

    )


    inmueble = get_object_or_404(

        Inmueble,

        id=inmueble_id,

        arrendador=perfil

    )


    if request.method == 'POST':


        inmueble.publicado = not inmueble.publicado


        inmueble.save(

            update_fields=['publicado']

        )


    return redirect(

        'gestion_inmuebles:mis_inmuebles'

    )
