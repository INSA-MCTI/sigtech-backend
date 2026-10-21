from django.urls import path

from contracts import views

urlpatterns = [
    path('', views.index_contratos, name='index'),
]
