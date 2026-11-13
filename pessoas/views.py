# Create your views here.
import unicodedata

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from pessoas.forms import CadastroForm, EventoForm, LoginForm
from pessoas.models import Contato, Usuario, Evento

User = get_user_model()


def _gera_usuario(nome_completo):
    partes = nome_completo.strip().split()

    NUMERO_PARTES = 2

    if len(partes) < NUMERO_PARTES:
        raise ValueError('Informe o nome e pelo menos um sobrenome')

    nome = partes[0]
    sobrenome = partes[1]
    texto = f'{nome}.{sobrenome}'.lower()

    texto = unicodedata.normalize('NFKD', texto)
    texto = ''.join(
        caractere
        for caractere in texto
        if not unicodedata.combining(caractere)
    )

    return texto


def cadastro_usuario(request):
    form = CadastroForm()

    if request.method == 'POST':
        form = CadastroForm(request.POST)

        if form.is_valid():
            pessoa = form.save()

            Contato.objects.create(
                pessoa=pessoa,
                email=form.cleaned_data['email'],
                telefone=form.cleaned_data['telefone'],
            )

            usuario = _gera_usuario(pessoa.nome)

            conta = User.objects.create_user(
                username=usuario,
                email=form.cleaned_data['email'],
                password=form.cleaned_data['senha'],
                first_name=pessoa.nome,
            )

            Usuario.objects.create(pessoa=pessoa, conta=conta)

            messages.success(
                request,
                'Cadastro realizado com sucesso!',
            )

            return redirect('pessoas:inicio')

    return render(
        request,
        'pessoas/cadastro_usuario.html',
        {'form': form},
    )


def _eventos_visiveis(usuario):
    eventos = Evento.objects.select_related('criador')
    if not usuario.is_staff:
        eventos = eventos.filter(Q(criador=usuario) | Q(geral=True))
    return eventos.order_by('dt_inicio', 'pk')


def _pode_gerenciar_evento(usuario, evento):
    return usuario.is_staff or evento.criador_id == usuario.pk


@login_required(login_url='pessoas:login')
def agenda_usuario(request):
    pagina = Paginator(_eventos_visiveis(request.user), 20).get_page(
        request.GET.get('pagina')
    )
    for evento in pagina:
        evento.pode_gerenciar = _pode_gerenciar_evento(request.user, evento)
    return render(request, 'pessoas/agenda_usuario.html', {
        'eventos': pagina, 'pagina': pagina,
    })


@login_required(login_url='pessoas:login')
def criar_evento(request):
    form = EventoForm()
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.criador = request.user
            evento.save()
            
            messages.success(
                request,
                "Evento cadastrado com sucesso"
            )
            
            return redirect('pessoas:agenda_usuario')
    return render(request, 'pessoas/criar_evento.html', {
        'form': form, 'titulo': 'Novo evento',
    })


@login_required(login_url='pessoas:login')
def editar_evento(request, pk):
    evento = get_object_or_404(_eventos_visiveis(request.user), pk=pk)
    if not _pode_gerenciar_evento(request.user, evento):
        return HttpResponseForbidden('Você não pode editar este evento.')
    form = EventoForm(
        request.POST if request.method == 'POST' else None,
        instance=evento,
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Evento atualizado com sucesso.')
        return redirect('pessoas:agenda_usuario')
    return render(request, 'pessoas/criar_evento.html', {
        'form': form, 'titulo': 'Editar evento',
    })


@login_required(login_url='pessoas:login')
@require_POST
def excluir_evento(request, pk):
    evento = get_object_or_404(_eventos_visiveis(request.user), pk=pk)
    if not _pode_gerenciar_evento(request.user, evento):
        return HttpResponseForbidden('Você não pode excluir este evento.')
    evento.delete()
    messages.success(request, 'Evento excluído com sucesso.')
    return redirect('pessoas:agenda_usuario')


def evento_ferias(request):
    return render(request, 'pessoas/evento_ferias.html')


def login_usuario(request):
    """
    Rever Esse tópico
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            login = form.cleaned_data['login']
            senha = form.cleaned_data['senha']

            usuario = authenticate(request, username=login, password=senha)

            if usuario is not None:
                auth_login(request, usuario)
                return redirect('pessoas:agenda_usuario')

            form.add_error(None, 'Dados Inválidos')

    else:
        form = LoginForm()

    return render(request, 'pessoas/login.html', {'form': form})


def perfil_detalhado(request):
    return render(request, 'pessoas/perfil_detalhado.html')


def index_pessoas(request):
    return render(request, 'pessoas/inicio.html')
