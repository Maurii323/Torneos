from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages     # sistema de mensajes de django para mostrar errores o mensajes de confirmacion
from django.urls import reverse         # simplifica el redireccionamiento y permite enviar parametros
from django.core.paginator import Paginator     # divide listas en paginas de x elementos 
from django.db import IntegrityError
# importa el decorador que comprueba que el que accede a esa vista este logueado
from django.contrib.auth.decorators import login_required
# importa los modelos que estan relacionado a los clubes
from clubes.models import Club
# importa datetime para obtener la fecha de alta y baja del club
from datetime import datetime


# Muestra todos los clubes y le aplica los filtros pasados por parametros en GET
@login_required
def clubHome(request):
    clubes = Club.objects.filter(fechaBaja__isnull=True, user=request.user )  # filtra y obtiene los clubes activos del usuario logueado

    # Obtener parámetros de la URL de los filtros
    order = request.GET.get('order', '')            # order es el nombre del parametro, '' es lo que guarda si no existe
    categoria = request.GET.get('categoria', '')    # obtiene el id
    try:
        categoria = int(categoria)  # Intenta convertirlo a entero
    except (ValueError, TypeError):
        categoria = None
    search = request.GET.get('search', '')

    # Búsqueda por nombre
    if search:
        clubes = clubes.filter(nombre__icontains=search) # __icontains filtra los clubes que contienen la busqueda, la i hace que sea insensible a mayusculas

    # Filtrar por categoría segun el id pasado por parametro
    if categoria:
        clubes = clubes.filter(clubCategoriaId__id=categoria)

    # Ordenar por nombre
    if order == 'asc':
        clubes = clubes.order_by('nombre')  # Orden ascendente
    elif order == 'desc':
        clubes = clubes.order_by('-nombre')  # Orden descendente

    # Crea la Paginación con 10 objetos por página
    paginator = Paginator(clubes, 10)
    # Obtener el número de página desde la URL (si no existe, por defecto es la página 1)
    page_number = request.GET.get('page', 1)
    page_clubes = paginator.page(page_number)  # Obtener la página actual


    return render(request, 'clubes.html', {
        'clubes': page_clubes,
        'search': search,  # Para mostrar el valor actual de la búsqueda en el template
        'order': order,  # Para mostrar el orden actual en el template
    })


# Crear un club
@login_required
def createClub(request):
    p_nombre = request.POST['nombre']
    p_direccion = request.POST['direccion']
    p_telefono = request.POST['telefono']
    p_fechaAlta = datetime.now()
    p_user = request.user
    
    try:
        # Crea un club con el modelo correspondiente
        club = Club(
            user = p_user,
            nombre = p_nombre, 
            direccion= p_direccion, 
            telefono = p_telefono, 
            fechaAlta = p_fechaAlta, 
        )
        club.save()                 # Guarda ese usuario creado en la base de datos
        # envia ese mensaje con el sistema de mensajes de django
        messages.success(request, f"Se ha creado el club '{club.nombre}' exitosamente")
        return redirect(reverse('clubHome'))
    except IntegrityError as e:  # Captura específicamente errores de integridad
        messages.error(request, f"Ya tenes un club llamado '{club.nombre}'")
        return redirect(reverse('clubHome'))
    except Exception as e:
        messages.error(request, f"Error inesperado: {e}")
        return redirect(reverse('clubHome'))



# Eliminar un club
@login_required
def deleteClub(request, IDClub):
    try:
        club = get_object_or_404(Club, pk=IDClub)
        club.delete()
        messages.success(request, f"Se ha eliminado el club '{club.nombre}' exitosamente")
        return redirect(reverse('clubHome'))
    except Club.DoesNotExist:
        messages.error(request, f"error al eliminar el club, no existe")
        return redirect(reverse('clubHome'))


# muestra el detalle de un club y permite modificarlos
@login_required
def detailsClub(request, IDClub):
    club = get_object_or_404(Club, pk=IDClub)  
    try:
        club.nombre = request.POST['nombre']
        club.direccion = request.POST['direccion']
        club.telefono = request.POST['telefono']
        # actualiza el campo en la base de datos
        club.save()
        messages.success(request, f"Se ha modificado el club '{club.nombre}' exitosamente")
        return redirect(reverse('clubHome'))
    except Exception as e:
        messages.error(request, f"Error al actualizar el club: {str(e)}")
        return redirect(reverse('clubHome'))