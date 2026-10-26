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
    path('perfil_detalhado/', views.perfil_detalhado, name='perfil_detalhado'),
]
