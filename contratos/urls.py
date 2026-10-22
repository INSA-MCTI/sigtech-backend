from django.urls import path

from contratos import views

urlpatterns = [
    path('', views.index_contratos, name='index'),
]
