from django.db import models
from django.contrib.auth.models import User # importa el modelo User predeterminado por django
# importa los modelos que estan relacionado a los torneos
from clubes.models import Club

# Create your models here.
class Torneo(models.Model):
    nombre = models.CharField(null = False, max_length=100)
    user = models.ForeignKey(User,null = False, on_delete = models.CASCADE)
    fechaInicio = models.DateField(null = False)

    def __str__(self):
        return self.nombre
    
class Jornada(models.Model):
    numero = models.PositiveIntegerField(null = False)
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE)

    def __str__(self):
        return f'Jornada {self.numero} del Torneo {self.torneo.nombre}'

class Partido(models.Model):
    jornada = models.ForeignKey(Jornada, on_delete=models.CASCADE,null = False)
    # related_name define el nombre que se utilizará para acceder a los objetos del modelo de la clave foranea, cuando hay mas de 2 claves foraneas referenciando a una misma tabla, es necesario que esos 2 nombres sean distintos
    local = models.ForeignKey(Club, related_name='partidos_local', on_delete=models.CASCADE,null = False)
    visitante = models.ForeignKey(Club, related_name='partidos_visitante', on_delete=models.CASCADE,null = False)
    juegosLocal = models.IntegerField(null=True,blank=True)
    juegosVisitante = models.IntegerField(null=True,blank=True)
    fecha = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.local} vs {self.visitante} - {self.jornada}'