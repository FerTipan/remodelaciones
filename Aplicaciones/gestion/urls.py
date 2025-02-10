from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dash/', views.dash, name='dash'),
    path('dashboard1/', views.dashboard1, name='dashboard1'),
    path('api/datos_inmuebles/', views.datos_inmuebles, name='datos_inmuebles'),
    path('api/datos_reformas_cotizaciones/', views.datos_reformas_cotizaciones, name='datos_reformas_cotizaciones'),

    #propietario
    path('propietario/', views.nuevo_propietario, name='nuevo_propietario'),
    path('lista/propietario/', views.lista_propietario, name='lista_propietario'),
    path('editar/<int:propietario_id>/', views.editar_propietario, name='editar_propietario'),
    path('eliminar/<int:propietario_id>/', views.eliminar_propietario, name='eliminar_propietario'),

    #inmueble
    path('inmueble/', views.nuevo_inmueble, name='nuevo_inmueble'),
    path('lista/inmueble/', views.lista_inmueble, name='lista_inmueble'),
    path('editar/inmueble/<int:inmueble_id>/', views.editar_inmueble, name='editar_inmueble'),
    path('eliminar/inmueble/<int:inmueble_id>/', views.eliminar_inmueble, name='eliminar_inmueble'),

    #reformas
    path('reforma/', views.nueva_reforma, name='nueva_reforma'),
    path('lista/reforma/', views.lista_reforma, name='lista_reforma'),
    path('editar/reforma/<int:reforma_id>/', views.editar_reforma, name='editar_reforma'),
    path('eliminar/reforma/<int:reforma_id>/', views.eliminar_reforma, name='eliminar_reforma'),

    #cotizaciones
    path('cotizaciones/', views.listado_cotizaciones, name='listado_cotizacion'),
    path('cotizaciones/crear/', views.nueva_cotizacion, name='nueva_cotizacion'),
    path('cotizaciones/editar/<int:cotizacion_id>/', views.editar_cotizacion, name='editar_cotizacion'),
    path('cotizaciones/eliminar/<int:cotizacion_id>/', views.eliminar_cotizacion, name='eliminar_cotizacion'),
]