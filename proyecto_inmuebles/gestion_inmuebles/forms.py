from django import forms

from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm
)

from django.contrib.auth.models import User

from django.db.models import Q


from .models import (
    PerfilUsuario,
    SolicitudArriendo,
    HorarioVisita,
    Inmueble,
)


# ============================================================
# FORMULARIO DE REGISTRO
# ============================================================

class RegistroForm(UserCreationForm):

    first_name = forms.CharField(
        label='Nombre',
        max_length=150
    )

    last_name = forms.CharField(
        label='Apellido',
        max_length=150
    )

    email = forms.EmailField(
        label='Correo electrónico',
        max_length=150
    )

    rut = forms.CharField(
        label='RUT',
        max_length=12
    )

    direccion = forms.CharField(
        label='Dirección',
        max_length=255
    )

    telefono = forms.CharField(
        label='Teléfono',
        max_length=20
    )

    tipo_usuario = forms.ChoiceField(
        label='Tipo de usuario',
        choices=PerfilUsuario.TIPO_USUARIO_CHOICES
    )


    class Meta:

        model = User

        fields = [
            'first_name',
            'last_name',
            'email',
            'rut',
            'direccion',
            'telefono',
            'tipo_usuario',
            'password1',
            'password2',
        ]


    # ----------------------------------------------------------
    # VALIDAR CORREO
    # ----------------------------------------------------------

    def clean_email(self):

        email = self.cleaned_data['email'].lower()

        existe = User.objects.filter(
            Q(email__iexact=email) |
            Q(username__iexact=email)
        ).exists()


        if existe:

            raise forms.ValidationError(
                'Ya existe un usuario registrado con este correo.'
            )


        return email


    # ----------------------------------------------------------
    # VALIDAR RUT
    # ----------------------------------------------------------

    def clean_rut(self):

        rut = self.cleaned_data['rut']


        if PerfilUsuario.objects.filter(
            rut=rut
        ).exists():

            raise forms.ValidationError(
                'Ya existe un usuario registrado con este RUT.'
            )


        return rut


    # ----------------------------------------------------------
    # GUARDAR USER + PERFILUSUARIO
    # ----------------------------------------------------------

    def save(self, commit=True):

        user = super().save(
            commit=False
        )


        email = self.cleaned_data['email']


        user.username = email

        user.email = email

        user.first_name = self.cleaned_data[
            'first_name'
        ]

        user.last_name = self.cleaned_data[
            'last_name'
        ]


        if commit:

            user.save()


            PerfilUsuario.objects.create(

                user=user,

                rut=self.cleaned_data[
                    'rut'
                ],

                direccion=self.cleaned_data[
                    'direccion'
                ],

                telefono=self.cleaned_data[
                    'telefono'
                ],

                tipo_usuario=self.cleaned_data[
                    'tipo_usuario'
                ]

            )


        return user


# ============================================================
# FORMULARIO DE LOGIN
# ============================================================

class LoginForm(AuthenticationForm):

    username = forms.EmailField(
        label='Correo electrónico'
    )


# ============================================================
# FORMULARIO PARA EDITAR DATOS DEL USUARIO
# ============================================================

class EditarUsuarioForm(forms.ModelForm):

    class Meta:

        model = User

        fields = [
            'first_name',
            'last_name',
        ]


# ============================================================
# FORMULARIO PARA EDITAR DATOS DEL PERFIL
# ============================================================

class EditarPerfilForm(forms.ModelForm):

    class Meta:

        model = PerfilUsuario

        fields = [
            'direccion',
            'telefono',
        ]


# ============================================================
# FORMULARIO PARA PUBLICAR INMUEBLE
# ============================================================

class InmuebleForm(forms.ModelForm):

    class Meta:

        model = Inmueble

        fields = [
            'nombre',
            'descripcion',
            'imagen',
            'm2_construidos',
            'm2_totales',
            'estacionamientos',
            'habitaciones',
            'banos',
            'direccion',
            'comuna',
            'tipo_inmueble',
            'precio_mensual',
        ]


        widgets = {

            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre de la propiedad'
                }
            ),

            'descripcion': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': 'Describe la propiedad...'
                }
            ),

            'imagen': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control',
                    'accept': 'image/*'
                }
            ),

            'm2_construidos': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0
                }
            ),

            'm2_totales': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0
                }
            ),

            'estacionamientos': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0
                }
            ),

            'habitaciones': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0
                }
            ),

            'banos': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0
                }
            ),

            'direccion': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Dirección del inmueble'
                }
            ),

            'comuna': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'tipo_inmueble': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'precio_mensual': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0,
                    'step': '1'
                }
            ),

        }


        labels = {

            'nombre': 'Nombre del inmueble',

            'descripcion': 'Descripción',

            'imagen': 'Imagen principal',

            'm2_construidos': 'Metros cuadrados construidos',

            'm2_totales': 'Metros cuadrados totales',

            'estacionamientos': 'Estacionamientos',

            'habitaciones': 'Habitaciones',

            'banos': 'Baños',

            'direccion': 'Dirección',

            'comuna': 'Comuna',

            'tipo_inmueble': 'Tipo de inmueble',

            'precio_mensual': 'Precio mensual',

        }


# ============================================================
# FORMULARIO PARA QUE EL ARRENDADOR CREE HORARIOS
# ============================================================

class HorarioVisitaForm(forms.ModelForm):

    class Meta:

        model = HorarioVisita

        fields = [
            'fecha',
            'hora',
        ]


        widgets = {

            'fecha': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                }
            ),

            'hora': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control',
                }
            ),

        }


        labels = {

            'fecha': 'Fecha disponible',

            'hora': 'Hora disponible',

        }


# ============================================================
# FORMULARIO PARA RESERVAR UNA VISITA
# ============================================================

class ReservaVisitaForm(forms.ModelForm):

    horario = forms.ModelChoiceField(

        queryset=HorarioVisita.objects.none(),

        label='Horario disponible',

        empty_label='Selecciona un horario',

        widget=forms.Select(
            attrs={
                'class': 'form-select',
            }
        )

    )


    class Meta:

        model = SolicitudArriendo

        fields = [
            'horario',
            'comentarios',
        ]


        widgets = {

            'comentarios': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Puedes agregar un comentario...',
                }
            ),

        }


    # ----------------------------------------------------------
    # MOSTRAR SOLO HORARIOS DISPONIBLES
    # ----------------------------------------------------------

    def __init__(
        self,
        *args,
        inmueble=None,
        **kwargs
    ):

        super().__init__(
            *args,
            **kwargs
        )


        if inmueble:

            self.fields['horario'].queryset = (
                HorarioVisita.objects.filter(
                    inmueble=inmueble,
                    disponible=True
                )
                .order_by(
                    'fecha',
                    'hora'
                )
            )


# ============================================================
# FORMULARIO PARA MODIFICAR UNA VISITA
# ============================================================

class EditarSolicitudForm(forms.ModelForm):

    horario = forms.ModelChoiceField(

        queryset=HorarioVisita.objects.none(),

        label='Horario de visita',

        empty_label='Selecciona un horario',

        widget=forms.Select(
            attrs={
                'class': 'form-select',
            }
        )

    )


    class Meta:

        model = SolicitudArriendo

        fields = [
            'horario',
            'comentarios',
        ]


        widgets = {

            'comentarios': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Puedes agregar un comentario...',
                }
            ),

        }


    # ----------------------------------------------------------
    # HORARIOS DISPONIBLES PARA CAMBIAR LA VISITA
    # ----------------------------------------------------------

    def __init__(
        self,
        *args,
        inmueble=None,
        **kwargs
    ):

        super().__init__(
            *args,
            **kwargs
        )


        if inmueble:

            horarios = HorarioVisita.objects.filter(
                inmueble=inmueble,
                disponible=True
            )


            # También mostramos el horario actual
            if (
                self.instance
                and self.instance.pk
                and self.instance.horario_id
            ):

                horarios = HorarioVisita.objects.filter(

                    Q(
                        inmueble=inmueble,
                        disponible=True
                    )

                    |

                    Q(
                        id=self.instance.horario_id
                    )

                )


            self.fields['horario'].queryset = (
                horarios
                .distinct()
                .order_by(
                    'fecha',
                    'hora'
                )
            )