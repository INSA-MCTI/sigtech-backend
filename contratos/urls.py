from django.contrib import admin
from django.urls import include, path
from contratos import views

urlpatterns = [
    path('', views.index_contratos, name='index'),
]
