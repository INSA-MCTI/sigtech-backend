# Create your views here.
from django.shortcuts import render


def index_contratos(request):
    return render(request, 'contratos/index.html')
