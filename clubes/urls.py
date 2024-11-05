from django.urls import path
from . import views

urlpatterns = [
    path('', views.clubHome, name="clubHome"),
    path('crearClub', views.createClub, name="createClub"),
    path('deleteClub/<int:IDClub>/', views.deleteClub, name="deleteClub"),
    path('detailsClub/<int:IDClub>/', views.detailsClub, name="detailsClub"),

]