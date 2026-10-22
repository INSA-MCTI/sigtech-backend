from django.urls import path

from pessoas import views

urlpatterns = [
    path('', views.index_pessoas, name='index'),
    path('login/', views.login_usuario, name='login'),
]
