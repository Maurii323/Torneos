from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
#funciones para crear sesion, autenticar si un usuario esta registrado, y cerrar una sesion
from django.contrib.auth import login , authenticate, logout
# el acceso a vistas que requieran login a usuarios logueados
from django.contrib.auth.decorators import login_required

# registracion de users
def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username=username, password=password1)    # Crea un usuario con la contraseña hasheada
                user.save()                                             # Guarda ese usuario creado en la base de datos
                login(request, user)                                    # Crea una cookie de sesión con el usuario autenticado 
                # Redirecciona con un parametro, el mismo se añade en la url
                return redirect('home', username = username)
            except IntegrityError:          # maneja la excepcion de que el usuario ya existe en la base de datos
                return render(request,'signup.html',{             
                    'error' : 'El nombre de usuario ya existe'
                })
        return render(request,'signup.html',{
            'error' : 'Las contraseñas no coinciden'
        })

# logueo de users
def user_login(request):
    if request.method == 'GET':
        # Envia el formulario para loguearse
        return render(request, 'login.html', {
            'form': AuthenticationForm
        })
    else:
        # Comprueba si el usuario y la contraseña son correctos
        p_username = request.POST['username']
        p_password = request.POST['password']
        user = authenticate( request, username= p_username, password= p_password)
        if user is None:    # si fallo la autenticacion
            return render (request, 'login.html',{
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrecta'
            })
        else:
            # Crea la sesion
            login(request, user)
            return redirect('home', username = p_username)

# cierre de sesion
@login_required
def user_logout(request):
    logout(request)        #elimina el cookie con la sesion activa del usuario
    return redirect('login')

# home
def home(request, username = None):
    if username == None:
        return render(request, 'home.html')
    else:
        return render(request, 'home.html', {
            'username' : username
        })



