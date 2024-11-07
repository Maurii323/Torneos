from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages     # sistema de mensajes de django para mostrar errores o mensajes de confirmacion
from django.urls import reverse         # simplifica el redireccionamiento y permite enviar parametros
from django.core.paginator import Paginator     # divide listas en paginas de x elementos 

# importa el decorador que comprueba que el que accede a esa vista este logueado
from django.contrib.auth.decorators import login_required
# importa los modelos que estan relacionado a los clubes
from clubes.models import Club
from padron.models import Padron,Tipo_doc
# importa datetime para obtener la fecha de alta y baja del club
from datetime import datetime


# Muestra todos los clubes y le aplica los filtros pasados por parametros en GET
@login_required
def padronHome(request):
    padron = Padron.objects.filter(fechaBaja__isnull=True, user=request.user)
    clubes = Club.objects.filter(fechaBaja__isnull=True, user=request.user )
    # Obtener parámetros de la URL de los filtros
    order = request.GET.get('order', '')            # order es el nombre del parametro, '' es lo que guarda si no existe
    
    categoria = request.GET.get('categoria', '')    # obtiene el id
    try:
        categoria = int(categoria)  # Intenta convertirlo a entero
    except (ValueError, TypeError):
        categoria = None

    search = request.GET.get('search', '')

    # Búsqueda por club
    if search:
        padron = padron.filter(club__nombre__icontains=search) # __icontains filtra los clubes que contienen la busqueda(nombre), la i hace que sea insensible a mayusculas

    # Filtrar por categoría segun el id pasado por parametro
    if categoria:
        padron = padron.filter(clubCategoriaId__id=categoria)

    # Ordenar por nombre
    if order == 'asc':
        padron = padron.order_by('nombre')  # Orden ascendente
    elif order == 'desc':
        padron = padron.order_by('-nombre')  # Orden descendente

    # Crea la Paginación con 10 objetos por página
    paginator = Paginator(padron, 10)
    # Obtener el número de página desde la URL (si no existe, por defecto es la página 1)
    page_number = request.GET.get('page', 1)
    page_padron = paginator.page(page_number)  # Obtener la página actual

    # Obtiene las categorias para pasarlas por parametro, y que en la plantilla se muestre como opcion de filtrado
    return render(request, 'padron.html', {
        'padron': page_padron,
        'search': search,  # Para mostrar el valor actual de la búsqueda en el template
        'order': order,  # Para mostrar el orden actual en el template
        'clubes': clubes,
    })

# Nuevo jugador
@login_required
def createJugador(request):

    clubes = Club.objects.all()
    if request.method == 'POST':
        p_user = request.user
        p_nombre = request.POST.get('nombre')
        p_apellido = request.POST.get('apellido')  
        p_idTipoDoc = Tipo_doc.objects.get(tipoDoc = request.POST.get('opciones'))
        p_nroDoc = request.POST.get('Documento') 
        p_club = request.POST.get('club')
        p_email = request.POST.get('email')  
        p_fechaNacimiento = request.POST.get('fechaNacimiento')  

     
        if not all([p_nombre, p_apellido, p_idTipoDoc, p_club, p_nroDoc, p_email, p_fechaNacimiento]):
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('padronHome')  

        try:
            # Crear nuevo jugador
            nuevo_jugador = Padron(
                user = p_user,
                nombre=p_nombre,
                apellido=p_apellido,
                idTipoDoc=p_idTipoDoc,
                club_id=p_club,
                nroDoc=p_nroDoc,
                email=p_email,
                fechaNacimiento=p_fechaNacimiento,
            )
            nuevo_jugador.save()
            
            messages.success(request, f"Se ha creado un jugador '{nuevo_jugador.nombre}' exitosamente")
            return redirect(reverse('padronHome'))
        except Exception as e:                      
            messages.error(request, f"{e}")
            return redirect(reverse('padronHome'))
    context = {
        'clubes': clubes,
    }
    return render(request, 'abmpadron.html', context)


# Eliminar un club
@login_required
def deleteJugador(request, IDJugador):
    try:
        jugador = get_object_or_404(Padron, pk=IDJugador)
        jugador.delete()
        messages.success(request, f"Se ha eliminado el jugador '{jugador.nombre}' exitosamente")
        return redirect(reverse('padronHome'))
    except Club.DoesNotExist:
        messages.error(request, f"error al eliminar el jugador, no existe")
        return redirect(reverse('padronHome'))


# muestra el detalle de un club y permite modificarlos
@login_required
def detailsJugador(request, IDJugador):
    jugador = get_object_or_404(Padron, pk=IDJugador)  
    try:
        jugador.nombre = request.POST['nombre']
        jugador.apellido = request.POST['apellido']
        jugador.idTipoDoc = Tipo_doc.objects.get(tipoDoc = request.POST.get('idTipoDoc'))
        jugador.nroDoc = request.POST.get('nroDoc')
        clubID = request.POST.get('club')
        club = get_object_or_404(Club, pk=clubID)  
        jugador.club = club
        jugador.email = request.POST.get('email') 
        jugador.fechaNacimiento = request.POST.get('fechaNacimiento')
        # actualiza el campo en la base de datos
        jugador.save()
        messages.success(request, f"Se ha modificado el jugador '{jugador.nombre}' exitosamente")
        return redirect(reverse('padronHome'))
    except Exception as e:
        messages.error(request, f"Error al actualizar el jugador: {str(e)}")
        return redirect(reverse('padronHome'))
    