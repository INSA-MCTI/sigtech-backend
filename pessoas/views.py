# Create your views here.
# Create your views here.
from django.shortcuts import render


def index_pessoas(request):
    return render(request, 'pessoas/index.html')
