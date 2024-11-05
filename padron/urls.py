from django.urls import path
from . import views

urlpatterns = [
    path('', views.padronHome, name="padronHome"),
    path('createJugador', views.createJugador, name="createJugador"),
    path('deleteJugador/<int:IDJugador>', views.deleteJugador, name="deleteJugador"),
    path('detailsJugador/<int:IDJugador>', views.detailsJugador, name="detailsJugador"),

]