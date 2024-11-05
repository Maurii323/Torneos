from django.contrib import admin
from .models import Padron, Tipo_doc

# Register your models here.
admin.site.register(Tipo_doc)
admin.site.register(Padron)