from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import datetime

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=255)
    cuerpo = RichTextField()
    imagen = models.ImageField(upload_to='images/', blank=True)
    fechaPublicacion = models.DateTimeField(auto_now_add=True)
    autor = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title

class Page(models.Model):
    title = models.CharField(max_length=200)
    contenido = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    fechaCreacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    imagen = models.ImageField(default='default.jpg', upload_to='profilePics')
    nombre = models.CharField(max_length=100, blank=True)
    descripcion = models.TextField(blank=True)
    sitioWeb = models.URLField(blank=True)
    email = models.EmailField(blank=True)


    def __str__(self):
        return f'{self.usuario.username} Perfil'