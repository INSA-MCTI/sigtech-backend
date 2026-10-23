from django.urls import path

from pessoas import views

app_name = 'pessoas' # Namespace para rotas

urlpatterns = [
    path('', views.index_pessoas, name='index'),
    path('pessoas/login/', views.login_usuario, name='login'),
    path('pessoas/cadastro_usuario/', views.cadastro_usuario, name='cadastro_usuario'),
]
