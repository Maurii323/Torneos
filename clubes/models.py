from django.db import models
from django.contrib.auth.models import User # importa el modelo User predeterminado por django

# Create your models here.
class Club(models.Model):
    # El id como primary key lo genera automaticamente django
    user = models.ForeignKey(User,null = False, on_delete = models.CASCADE)
    nombre = models.CharField(max_length = 45, null = False, unique=True)  # no puede ser nulo, es unico
    direccion = models.CharField(max_length = 45, null = False)
    telefono = models.CharField(max_length = 45, null = False)
    fechaAlta = models.DateTimeField(null = False)
    fechaBaja = models.DateTimeField(null = True, blank = True) # Puede ser Null
 
    def __str__(self):
        return self.nombre