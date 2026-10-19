from django.http import HttpResponse

# Create your views here.


def ver_funcionario(request):
    return HttpResponse('Funcionário!')
