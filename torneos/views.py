from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
import random
# importa el decorador que comprueba que el que accede a esa vista este logueado
from django.contrib.auth.decorators import login_required
# importa los modelos que estan relacionado a los torneos
from clubes.models import Club
from torneos.models import Torneo,Jornada,Partido
# importa datetime para obtener la fecha actual
from datetime import datetime

# Muestra las jornadas del torneo seleccionado, si no tiene un id de torneo como parametro, muestra los torneos disponibles
@login_required
def torneoHome(request,IDTorneo = None):
    # Obtiene todos los torneos para poder seleccionarlos
    torneos = Torneo.objects.filter(user = request.user)
    
    # Si no se paso id por parametro, solamente retorna los torneos, si se pasó retorna sus jornadas y partidos
    if IDTorneo is None:
        return render(request, 'torneos.html', {
            'torneos': torneos,          # retorna los torneos para seleccionarlos 
        })
    else:
        torneo = get_object_or_404(Torneo, pk=IDTorneo)
        jornadas = Jornada.objects.filter(torneo=torneo)
        #devuelve todos los partidos de las jornadas del torneo correspondiente
        partidos = Partido.objects.filter(jornada__in = jornadas) 

        # Crea la Paginación, cada pagina tiene 1 jornada
        paginator = Paginator(jornadas, 1)
        # Obtener el número de página desde la URL (si no existe, por defecto es la página 1)
        page_number = request.GET.get('page', 1)
        page_jornadas = paginator.page(page_number)  # Obtener la página actual
        # Obtener la jornada actual
        jornada_actual = page_jornadas.object_list[0]  # Solo hay una jornada por página
        # Obtener los partidos relacionados a la jornada actual con el related manager(atributo para acceder a los objetos relacionados con la foreign key)
        partidos = jornada_actual.partido_set.all()

    return render(request, 'torneos.html', {
        'torneos': torneos,          # retorna los torneos para seleccionarlos 
        'torneo': torneo,
        'jornadas': page_jornadas,
        'partidos': partidos,
        'jornada_actual': jornada_actual
    })


# Crear un torneo, generando su fixture
@login_required
def createTorneo(request):
    p_nombre=request.POST['nombre']
    p_user = request.user
    p_fechaInicio = datetime.now()

    try:
        torneo = Torneo(                # crea el torneo
            nombre = p_nombre,
            user = p_user, 
            fechaInicio = p_fechaInicio
        )
        torneo.save()
        # algoritmo para generar el fixture
        clubes = list(Club.objects.filter())
        # maneja la excepcion de que no hayan 2 clubes o mas
        if len(clubes) < 2:
            raise ValueError("Se necesitan al menos 2 clubes para generar un fixture.")
        # Para que funcione si el número de equipos es impar(agrega un equipo fantasma para la fecha libre)
        if len(clubes) % 2 != 0:
            clubes.append(None)  

        random.shuffle(clubes)  # Mezclar los equipos de forma aleatoria

        with transaction.atomic():  #transacción atómica para asegurar que la creación de jornadas y partidos se realice de manera consistente y evitar problemas de integridad de datos.
            alternar_localia = True  # Define si los equipos impares empiezan como locales o visitantes
            for jornada_num in range(1, len(clubes)):
                jornada = Jornada.objects.create(numero=jornada_num, torneo=torneo) # crea la jornada
                # genera los partidos de esa jornada
                for i in range(len(clubes) // 2):   
                    if alternar_localia:
                        equipo_local = clubes[i]
                        equipo_visitante = clubes[-(i+1)]
                    else:
                        equipo_local = clubes[-(i+1)]
                        equipo_visitante = clubes[i]

                    if equipo_local and equipo_visitante:  # Ignorar si es el equipo fantasma(tiene fecha libre)
                        Partido.objects.create(jornada=jornada, local=equipo_local, visitante=equipo_visitante, juegosLocal = None, juegosVisitante = None)
                
                # Rotar los equipos para la siguiente jornada (round-robin)
                clubes = [clubes[0]] + [clubes[-1]] + clubes[1:-1]
                # Alternar la localía para la próxima jornada
                alternar_localia = not alternar_localia

        # envia ese mensaje con el sistema de mensajes de django
        messages.success(request, f"Se ha creado el Torneo '{torneo.nombre}' exitosamente")
        return redirect(reverse('torneoHome'))
    except Exception as e:
        messages.error(request, f"Error al crear el torneo: {str(e)}")
        return redirect(reverse('torneoHome'))
    except IntegrityError:                         # maneja la excepcion de que el torneo ya existe en la base de datos
        messages.error(request, f"el nombre del torneo ingresado ya existe")
        return redirect(reverse('torneoHome'))
    

# permite modificar un partido actualizando el puntaje de cada equipo
@login_required
def modificarPartido(request, IDPartido):
    partido = get_object_or_404(Partido, pk=IDPartido)
    golesLocal = request.POST['local']
    golesVisita = request.POST.get('visitante')

    # Valida que los goles sean numeros positivos
    try:
        if int(golesLocal) < 0 or int(golesVisita) < 0:
            messages.error(request, f"Error al actualizar el partido: Ingreso un valor negativo")
            return redirect(reverse('torneoHome'))
    except:
        messages.error(request, f"Error al actualizar el partido: No ingreso un valor numerico")
        return redirect(reverse('torneoHome'))
    
    # Realiza la actualizacion del partido
    try:
        partido.juegosLocal = golesLocal
        partido.juegosVisitante = golesVisita
        partido.save()
        # de que torneo pertenece el partido
        torneo = partido.jornada.torneo
        messages.success(request, f"Se ha modificado el partido {partido.local} - {partido.visitante} exitosamente")
        return redirect(reverse('torneoHome', kwargs={'IDTorneo': torneo.id}))
    except Exception as e:
        messages.error(request, f"Error al actualizar el partido: {str(e)}")
        return redirect(reverse('torneoHome'))


# Muestra la tabla de posiciones del torneo seleccionado, si no tiene un id de torneo como parametro, muestra los torneos disponibles
@login_required
def tablasHome(request,IDTorneo = None):
    # Obtiene todos los torneos para poder seleccionarlos
    torneos = Torneo.objects.filter()
    
    # Si no se paso id por parametro, solamente retorna los torneos, si se pasó retorna la tabla de posiciones
    if IDTorneo is None:
        return render(request, 'tablasTorneo.html', {
        'torneos': torneos          # retorna los torneos para seleccionarlos 
        })
    else:
        torneo = get_object_or_404(Torneo, pk=IDTorneo)
        jornadas = Jornada.objects.filter(torneo=torneo)
        #devuelve todos los partidos de las jornadas del torneo correspondiente
        partidos = Partido.objects.filter(jornada__in = jornadas) 
        
        # Crear un diccionario para almacenar las estadísticas de cada club
        posiciones = {}

        for partido in partidos:
            # Determinar el resultado del partido
            juegos_local = partido.juegosLocal
            juegos_visitante = partido.juegosVisitante
            
            # Saltar partidos sin resultado
            if juegos_local is None or juegos_visitante is None:
                continue
            
            # Inicializar los clubes si no están en el diccionario(primera jornada)
            if partido.local not in posiciones:
                posiciones[partido.local] = {'posicion': None, 'club': partido.local, 'diferenciaJuegos': 0,'partidosEmpatados' : 0,
                                         'partidosJugados' : 0,'partidosGanados' : 0,'partidosPerdidos' : 0, 'puntaje': 0}
            if partido.visitante not in posiciones:
                posiciones[partido.visitante] = {'club': partido.visitante, 'diferenciaJuegos': 0,'partidosEmpatados' : 0,
                                        'partidosJugados' : 0,'partidosGanados' : 0,'partidosPerdidos' : 0, 'puntaje': 0}
            
            # Suma el partido jugado
            posiciones[partido.local]['partidosJugados'] += 1 
            posiciones[partido.visitante]['partidosJugados'] += 1

            # Comparar los goles para determinar el ganador
            if juegos_local > juegos_visitante:                 # El equipo local ganó el partido
                # suma la diferencia positiva de goles al ganador(local), suma un partido ganado y +3 puntos
                posiciones[partido.local]['diferenciaJuegos'] += (juegos_local - juegos_visitante)
                posiciones[partido.local]['partidosGanados'] += 1
                posiciones[partido.local]['puntaje'] += 3 
                # resta la diferencia negativa de goles al perdedor(visitante) y suma un partido perdido
                posiciones[partido.visitante]['diferenciaJuegos'] -= (juegos_local - juegos_visitante) 
                posiciones[partido.visitante]['partidosPerdidos'] += 1
            elif juegos_local < juegos_visitante:                # El equipo visitante ganó el partido
                # suma la diferencia positiva de goles al ganador(visita), suma un partido ganado y +3 puntos
                posiciones[partido.visitante]['diferenciaJuegos'] += (juegos_visitante - juegos_local)
                posiciones[partido.visitante]['partidosGanados'] += 1
                posiciones[partido.visitante]['puntaje'] += 3
                # resta la diferencia negativa de goles al perdedor(visitante) y suma un partido perdido
                posiciones[partido.local]['diferenciaJuegos'] -= (juegos_visitante - juegos_local)
                posiciones[partido.local]['partidosPerdidos'] += 1
            else:   # empate
                posiciones[partido.local]['puntaje'] += 1
                posiciones[partido.visitante]['puntaje'] += 1
                posiciones[partido.local]['partidosEmpatados'] += 1
                posiciones[partido.visitante]['partidosEmpatados'] += 1

        # Ordenar los clubes por puntaje y juegos ganados
        posiciones_ordenadas = sorted(posiciones.values(), key=lambda x: (-x['puntaje'], -x['diferenciaJuegos']))
        # Segun su posicion en el diccionario, agrega su posicion en la tabla
        for indice, posicion in enumerate(posiciones_ordenadas):
            posicion['posicion'] = indice + 1

        # Crea la Paginación con 10 objetos por página
        paginator = Paginator(posiciones_ordenadas, 10)
        # Obtener el número de página desde la URL (si no existe, por defecto es la página 1)
        page_number = request.GET.get('page', 1)
        page_tabla = paginator.page(page_number)  # Obtener la página actual

    return render(request, 'tablasTorneo.html', {
        'torneos': torneos,          # retorna los torneos para seleccionarlos 
        'torneo': torneo,
        'posiciones': page_tabla    })
