from django.urls import path

from pessoas import views

app_name = 'pessoas'  # Namespace para rotas

urlpatterns = [
    path('', views.index_pessoas, name='inicio'),
    path('login/', views.login_usuario, name='login'),
    path(
        'cadastro_usuario/',
        views.cadastro_usuario,
        name='cadastro_usuario',
    ),
    path('agenda_usuario/', views.agenda_usuario, name='agenda_usuario'),
    path('criar_evento/', views.criar_evento, name='criar_evento'),
]
