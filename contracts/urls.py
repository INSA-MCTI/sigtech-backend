from django.urls import path
from . import views

urlpatterns = [
    path("ver/", views.ver_contrato, name="ver_contrato"),
]
