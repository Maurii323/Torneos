from django.urls import path
from . import views

urlpatterns = [
    path('', views.torneoHome, name="torneoHome"),
    path('<int:IDTorneo>/', views.torneoHome, name="torneoHome"),
    path('crearTorneo/', views.createTorneo, name="createTorneo"),
    path('eliminarTorneo/<int:IDTorneo>', views.deleteTorneo, name="deleteTorneo"),
    path('modificarPartido/<int:IDPartido>/', views.modificarPartido, name="modificarPartido"),
    path('tablas/', views.tablasHome, name="tablasHome"),
    path('tablas/<int:IDTorneo>/', views.tablasHome, name="tablasHome"),
]