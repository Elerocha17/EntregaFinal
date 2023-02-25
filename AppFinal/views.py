from django.shortcuts import get_object_or_404, render, redirect
from AppFinal.forms import UserRegisterForm, PerfilForm
from AppFinal.models import Blog, Perfil
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from AppFinal.forms import BlogForm, Perfil, UserUpdateForm, ProfileUpdateForm
import os
from django.template.loader import render_to_string
from django.conf import settings
from django.shortcuts import render
from .forms import ContactForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


# Create your views here.


#def inicio(request):
    #return render(request, "AppFinal/inicio.html")

def pages(request):
    return render(request, "AppFinal/pages.html")

def about(request):
    return render(request, "AppFinal/about.html")

def padre(request):
    return render(request, "AppFinal/Padre.html")

def cerrarSesion(request):
    logout(request)
    return redirect('Inicio')

def login_request(request):

    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)

        if form.is_valid():  # Si pasó la validación de Django

            usuario = form.cleaned_data.get('username')
            contrasenia = form.cleaned_data.get('password')

            user = authenticate(username= usuario, password=contrasenia)

            if user is not None:
                login(request, user)

                return render(request, "AppFinal/inicio.html", {"mensaje":f"Bienvenido {usuario}"})
            else:
                return render(request, "AppFinal/inicio.html", {"mensaje":"Datos incorrectos"})
           
        else:

            return render(request, "AppFinal/inicio.html", {"mensaje":"Formulario erroneo"})

    form = AuthenticationForm()

    return render(request, "AppFinal/login.html", {"form": form})

def register(request):

      if request.method == 'POST':

            #form = UserCreationForm(request.POST)
            form = UserRegisterForm(request.POST)
            if form.is_valid():

                  username = form.cleaned_data['username']
                  form.save()
                  return render(request,"AppFinal/inicio.html" ,  {"mensaje":"Usuario Creado :)"})

      else:
            #form = UserCreationForm()       
            form = UserRegisterForm()     

      return render(request,"AppFinal/registro.html" ,  {"form":form})

@login_required
def perfilUsuario(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = PerfilForm(request.POST, request.FILES, instance=request.user.perfil)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Tu cuenta ha sido actualizada.')
            return redirect('perfil')
        else:
            messages.error(request, f'Por favor corrige los errores a continuación.')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = PerfilForm(instance=request.user.perfil)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'AppFinal/perfil.html', context)

def crearBlog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.save()
            
            # Renderiza el contenido del blog en un template
            blog_template = render_to_string('blogs/blogDetalle.html', {'blog': blog})
            
            # Crea un archivo nuevo para el template del blog
            template_path = os.path.join(settings.BASE_DIR, 'AppFinal','templates', 'blogs', f'blog_{blog.id}.html')
            with open(template_path, 'w') as f:
                f.write(blog_template)
            
            return redirect('blogLista')
    else:
        form = BlogForm()
    return render(request, 'AppFinal/crearBlog.html', {'form': form})

def blogLista(request):
    blogs = Blog.objects.all()
    context = {'blogs': blogs}
    return render(request, 'AppFinal/blogLista.html', context)

def inicio(request):
    blogs = Blog.objects.all()
    context = {
        'blogs': blogs,
    }
    return render(request, 'AppFinal/inicio.html', context)

def seccionLista(request):
    blogs = Blog.objects.all()
    template = ('AppFinal/blogLista.html', {'blogs': blogs})
    return render(request, *template)

def blogDetalle(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'blogs/blogDetalle.html', {'blog': blog})

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'AppFinal/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        # otras variables de contexto aquí
        return context