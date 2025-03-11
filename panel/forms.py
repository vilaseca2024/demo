from django import forms
from django.contrib.auth.models import User

class EmpleadoForm(forms.ModelForm):
    # Campos adicionales para el formulario
    area_choices = [
        ('Contabilidad', 'Contabilidad'),
        ('Operaciones', 'Operaciones'),
        ('Calidad', 'Calidad'),
        ('Gerencia', 'Gerencia'),
    ]
    
    rol_choices = [
        ('Administrador', 'Administrador'),
        ('Empleado', 'Empleado'),
    ]

    area = forms.ChoiceField(choices=area_choices, required=True, label="Área")
    tipo_usuario = forms.ChoiceField(choices=rol_choices, required=True, label="Tipo de Usuario")
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña", required=True)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
    
    def __init__(self, *args, **kwargs):
        super(EmpleadoForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "Nombre(s)"
        self.fields['last_name'].label = "Apellido(s)"
        self.fields['email'].label = "Correo electrónico"
        self.fields['username'].label = "Usuario"
