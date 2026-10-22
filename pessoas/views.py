# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect, render

from pessoas.forms import LoginForm


def login_usuario(request):

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            login = form.cleaned_data['login']
            senha = form.cleaned_data['senha']

            usuario = authenticate(request, username=login, password=senha)

            if usuario is not None:
                auth_login(request, usuario)
                return redirect('index')
            messages.error(request, 'Login ou senha inválidos.')

        else:
            form = LoginForm()

    return render(request, 'pessoas/login.html', {'form': form})


def index_pessoas(request):
    return render(request, 'pessoas/index.html')
