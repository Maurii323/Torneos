from django.db import models
from django.contrib.auth.models import User # importa el modelo User predeterminado por django

# Create your models here.
from clubes.models import Club

class Tipo_doc(models.Model):
    id = models.IntegerField(primary_key = True)
    tipoDoc = models.CharField(max_length = 45)
    descripcion = models.CharField(max_length = 200)

    def __str__(self):
        return self.tipoDoc

class Padron(models.Model):
    id = models.IntegerField(primary_key = True)
    user = models.ForeignKey(User,null = False, on_delete = models.CASCADE)
    idTipoDoc = models.ForeignKey(Tipo_doc, null = False, on_delete = models.PROTECT) # no permite que se borre ese atributo en la tabla club_Categoria.
    nroDoc = models.IntegerField(null = False)
    nombre = models.CharField(max_length = 45, null = False)
    apellido = models.CharField(max_length = 45, null = False)
    fechaNacimiento = models.DateField(null = False)
    email = models.CharField(max_length = 45, null = False)
    club = models.ForeignKey(Club, null = False, on_delete = models.CASCADE)
    fechaBaja = models.DateTimeField(null = True, blank = True)
    motivoBaja = models.CharField(max_length = 200, null = True, blank = True)

    def __str__(self):
        return self.nombre