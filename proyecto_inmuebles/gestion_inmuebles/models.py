from django.db import models
from django.contrib.auth.models import User


# ============================================================
# REGIÓN
# ============================================================

class Region(models.Model):

    nombre = models.CharField(
        max_length=50
    )

    def __str__(self):
        return self.nombre


# ============================================================
# COMUNA
# ============================================================

class Comuna(models.Model):

    nombre = models.CharField(
        max_length=100
    )

    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.nombre


# ============================================================
# PERFIL DE USUARIO
# ============================================================

class PerfilUsuario(models.Model):

    TIPO_USUARIO_CHOICES = [

        ('arrendatario', 'Arrendatario'),

        ('arrendador', 'Arrendador'),

    ]


    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil'
    )


    rut = models.CharField(
        max_length=12,
        unique=True,
        verbose_name="RUT"
    )


    direccion = models.CharField(
        max_length=255,
        verbose_name="Dirección"
    )


    telefono = models.CharField(
        max_length=20,
        verbose_name="Teléfono Personal"
    )


    tipo_usuario = models.CharField(
        max_length=20,
        choices=TIPO_USUARIO_CHOICES,
        default='arrendatario',
        verbose_name="Tipo de Usuario"
    )


    def __str__(self):
        return self.user.username


# ============================================================
# TIPO DE INMUEBLE
# ============================================================

class TipoInmueble(models.Model):

    nombre = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Tipo de Inmueble"
    )


    def __str__(self):
        return self.nombre


# ============================================================
# INMUEBLE
# ============================================================

class Inmueble(models.Model):

    nombre = models.CharField(
        max_length=200
    )


    descripcion = models.TextField()


    # ========================================================
    # IMAGEN PRINCIPAL DEL INMUEBLE
    # ========================================================

    imagen = models.ImageField(
        upload_to='inmuebles/',
        null=True,
        blank=True,
        verbose_name="Imagen principal"
    )


    m2_construidos = models.FloatField()


    m2_totales = models.FloatField()


    estacionamientos = models.IntegerField()


    habitaciones = models.IntegerField()


    banos = models.IntegerField()


    direccion = models.CharField(
        max_length=200
    )


    comuna = models.ForeignKey(
        Comuna,
        on_delete=models.CASCADE
    )


    tipo_inmueble = models.ForeignKey(
        TipoInmueble,
        on_delete=models.PROTECT,
        related_name='inmuebles',
        verbose_name="Tipo de Inmueble"
    )


    precio_mensual = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    
    publicado = models.BooleanField(
    default=True,
    verbose_name="Publicado"
    )


    arrendador = models.ForeignKey(
        PerfilUsuario,
        on_delete=models.CASCADE,
        related_name='inmuebles'
    )


    def __str__(self):
        return self.nombre


# ============================================================
# HORARIOS DISPONIBLES PARA VISITAR UN INMUEBLE
# ============================================================

class HorarioVisita(models.Model):

    # Propiedad a la que pertenece el horario
    inmueble = models.ForeignKey(
        Inmueble,
        on_delete=models.CASCADE,
        related_name='horarios_visita'
    )


    # Día disponible para visitar
    fecha = models.DateField()


    # Hora disponible para visitar
    hora = models.TimeField()


    # Indica si todavía puede ser reservado
    disponible = models.BooleanField(
        default=True
    )


    class Meta:

        # Evita que el arrendador cree dos veces
        # exactamente el mismo horario
        constraints = [

            models.UniqueConstraint(
                fields=[
                    'inmueble',
                    'fecha',
                    'hora'
                ],
                name='horario_visita_unico'
            )

        ]

        # Los mostramos ordenados por fecha y hora
        ordering = [
            'fecha',
            'hora'
        ]


    def __str__(self):

        return (
            f"{self.inmueble.nombre} - "
            f"{self.fecha} - "
            f"{self.hora}"
        )


# ============================================================
# SOLICITUD / RESERVA DE VISITA
# ============================================================

class SolicitudArriendo(models.Model):

    ESTADO_CHOICES = [
        ('reservada', 'Reservada'),
        ('cancelada', 'Cancelada'),
    ]


    arrendatario = models.ForeignKey(
        PerfilUsuario,
        on_delete=models.CASCADE,
        related_name='solicitudes'
    )

    inmueble = models.ForeignKey(
        Inmueble,
        on_delete=models.CASCADE,
        related_name='solicitudes'
    )

    horario = models.OneToOneField(
        HorarioVisita,
        on_delete=models.PROTECT,
        related_name='solicitud',
        null=True,
        blank=True
    )

    fecha_visita = models.DateField(
        null=True,
        blank=True
    )

    hora_visita = models.TimeField(
        null=True,
        blank=True
    )

    comentarios = models.TextField(
        blank=True
    )

    aceptada = models.BooleanField(
        default=False
    )


    # ========================================================
    # FECHA DE CREACIÓN
    # ========================================================

    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        null=True
    )


    # ========================================================
    # ESTADO DE LA SOLICITUD
    # ========================================================

    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='reservada'
    )


    # ========================================================
    # FECHA DE CANCELACIÓN
    # ========================================================

    fecha_cancelacion = models.DateTimeField(
        null=True,
        blank=True
    )


    # ========================================================
    # NOTIFICACIÓN DE RESERVA NUEVA
    # ========================================================

    vista_arrendador = models.BooleanField(
        default=False
    )


    # ========================================================
    # NOTIFICACIÓN DE CANCELACIÓN
    # ========================================================

    cancelacion_vista_arrendador = models.BooleanField(
        default=True
    )


    def __str__(self):

        return f"{self.arrendatario} - {self.inmueble}"