from django.forms import ModelForm, EmailInput
from aplicacionGeneral.models import Persona, Ordenes
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class RegistroUsuarioForm(UserCreationForm):
    #email = forms.EmailField()
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirma Contraseña', widget=forms.PasswordInput)
    class Meta:
        model = User  # Se relaciona con el modelo o tabla de Usuarios que viene por defecto en Django
        #fields = ['username','email','password1','password2'] # se seleccionan los campos
        fields = ['username','password1','password2'] # se seleccionan los campos
        help_texts = {k:"" for k in fields} # Se sobreescriben los textos de ayuda por espacio.

class PersonaForm(ModelForm):
    class Meta:
        model = Persona
        fields = '__all__'
        widgets = {
            'email': EmailInput(attrs={'type': 'email'})
        }

class PedidoForm(ModelForm):
    #direccion_orden = forms.CharField(label='Dirección Envío')
    #telefono_orden = forms.CharField(label='Teléfono')

    class Meta:
        model = Ordenes
        fields = ['direccion','telefono']
