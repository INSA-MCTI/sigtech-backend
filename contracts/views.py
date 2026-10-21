from django.shortcuts import render


def index_contratos(request):
    return render(request, 'contracts/index.html')
