from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, User
from django.contrib.auth.models import User
from ckeditor.widgets import CKEditorWidget
from AppFinal.models import Blog, Perfil
import datetime

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repetir contraseña", widget=forms.PasswordInput)
 
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        # Saca los mensajes de ayuda
        help_texts = {k:"" for k in fields}

# Clase 24, agregamos el UserEditForm
class PerfilForm(forms.ModelForm):
    imagen = forms.ImageField(label='Imagen', required=False)
    nombre = forms.CharField(label='Nombre', max_length=255)
    descripcion = forms.CharField(label='Descripción', widget=forms.Textarea)
    sitioWeb = forms.URLField(label='Link a la página web')
    email = forms.EmailField(label='Email')

    class Meta:
        model = Perfil
        fields = ('imagen', 'nombre', 'descripcion', 'sitioWeb', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].initial = self.instance.usuario.email

    def save(self, commit=True):
        perfil = super().save(commit=False)
        perfil.usuario.email = self.cleaned_data['email']
        if commit:
            perfil.save()
            perfil.usuario.save()
        return perfil


class BlogForm(forms.ModelForm):
    
    class Meta:
        model = Blog
        fields = ['title', 'cuerpo', 'imagen', 'autor']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['imagen', 'nombre', 'descripcion', 'sitioWeb', 'email',]

class ContactForm(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=100, required=True)
    email = forms.EmailField(label='Email', required=True)
    mensaje = forms.CharField(label='Mensaje', widget=forms.Textarea, required=True)