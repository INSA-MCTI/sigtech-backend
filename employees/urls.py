from django.urls import path

from . import views

urlpatterns = [
    path('ver/', views.ver_funcionario, name='ver_funcionario'),
]
