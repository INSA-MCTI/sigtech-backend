import csv
import io
import json
from datetime import date
from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Model, Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.urls import reverse

from .estatisticas import membros_indicador, relatorio_pessoal
from .forms import (
    ArquivoForm,
    DadoEstatisticoForm,
    EventoForm,
    ImportCSVForm,
    LoginForm,
    PessoaCargoForm,
    PessoaForm,
    PessoaUnidadeForm,
)
from .models import (
    Arquivo,
    DadoEstatistico,
    Evento,
    LogAuditoria,
    Pessoa,
    PessoaCargo,
    PessoaSituacaoHistorico,
    PessoaUnidade,
)


# ── Helpers ──────────────────────────────────────────────────────────

def _get_pessoa_logada(request):
    pessoa_id = request.session.get('pessoa_id')
    if not pessoa_id:
        return None
    try:
        return Pessoa.objects.get(pk=pessoa_id, deletado=False)
    except Pessoa.DoesNotExist:
        return None


def _login_required(view_func):
    def wrapper(request, *args, **kwargs):
        pessoa = _get_pessoa_logada(request)
        if not pessoa:
            return redirect('pessoas:login')
        request.pessoa = pessoa
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


def _nivel_required(*niveis_permitidos):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            pessoa = getattr(request, 'pessoa', None)
            if not pessoa or not pessoa.nivel_acesso:
                messages.error(request, 'Acesso negado.')
                return redirect('pessoas:dashboard')
            if pessoa.perfil_acesso not in [
                n.lower() for n in niveis_permitidos
            ]:
                messages.error(request, 'Acesso negado.')
                return redirect('pessoas:dashboard')
            return view_func(request, *args, **kwargs)
        wrapper.__name__ = view_func.__name__
        return wrapper
    return decorator


def _serializar_auditoria(dados):
    if dados is None or dados == '':
        return None
    if isinstance(dados, dict):
        dados = {
            chave: valor.pk if isinstance(valor, Model) else valor
            for chave, valor in dados.items()
            if chave not in {'senha', 'password'}
        }
    return json.dumps(dados, cls=DjangoJSONEncoder, ensure_ascii=False)


def _registrar_log(request, tabela, id_registro, acao,
                   dados_anteriores=None, dados_novos=None):
    acao = {
        'desativacao': 'desativar',
        'importacao_csv': 'importar',
    }.get(acao, acao)
    LogAuditoria.objects.create(
        pessoa=getattr(request, 'pessoa', None),
        tabela=tabela,
        id_registro=str(id_registro),
        acao=acao,
        dados_anteriores=_serializar_auditoria(dados_anteriores),
        dados_novos=_serializar_auditoria(dados_novos),
        ip=request.META.get('REMOTE_ADDR', ''),
    )


# ── Auth ─────────────────────────────────────────────────────────────

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            senha = form.cleaned_data['senha']
            try:
                pessoa = Pessoa.objects.get(
                    login=login, deletado=False
                )
            except Pessoa.DoesNotExist:
                messages.error(request, 'Login ou senha inválidos.')
                return render(
                    request, 'pessoas/login.html', {'form': form}
                )
            if check_password(senha, pessoa.senha):
                request.session['pessoa_id'] = pessoa.pk
                return redirect('pessoas:dashboard')
            messages.error(request, 'Login ou senha inválidos.')
    else:
        form = LoginForm()
    return render(request, 'pessoas/login.html', {'form': form})


def logout_view(request):
    request.session.flush()
    return redirect('pessoas:login')


# ── Dashboard ────────────────────────────────────────────────────────

@_login_required
def dashboard(request):
    total_pessoas = Pessoa.objects.filter(deletado=False).count()
    hoje = timezone.now()
    eventos_proximos = Evento.objects.filter(
        Q(geral=True) | Q(pessoa=request.pessoa),
        dt_inicio__gte=hoje,
    ).order_by('dt_inicio')[:5]
    return render(request, 'pessoas/dashboard.html', {
        'pessoa': request.pessoa,
        'total_pessoas': total_pessoas,
        'eventos_proximos': eventos_proximos,
    })


# ── CRUD Pessoa ──────────────────────────────────────────────────────

@_login_required
def pessoa_lista(request):
    q = request.GET.get('q', '')
    pessoas = Pessoa.objects.filter(deletado=False)
    if q:
        pessoas = pessoas.filter(
            Q(nome__icontains=q)
            | Q(matricula__icontains=q)
            | Q(cpf__icontains=q)
            | Q(email__icontains=q)
        )
    return render(request, 'pessoas/pessoa_lista.html', {
        'pessoas': pessoas,
        'q': q,
        'pessoa': request.pessoa,
    })


@_login_required
@_nivel_required('adm', 'rh')
@transaction.atomic
def pessoa_criar(request):
    if request.method == 'POST':
        form = PessoaForm(request.POST)
        if form.is_valid():
            pessoa = form.save(commit=False)
            senha = form.cleaned_data.get('senha')
            if senha:
                pessoa.senha = make_password(senha)
            pessoa.save()
            _registrar_log(
                request, 'pessoa', pessoa.pk, 'criacao',
                dados_novos=form.cleaned_data,
            )
            messages.success(request, 'Pessoa cadastrada com sucesso.')
            return redirect('pessoas:pessoa_detalhe', pk=pessoa.pk)
    else:
        form = PessoaForm()
    return render(request, 'pessoas/pessoa_form.html', {
        'form': form,
        'titulo': 'Cadastrar Pessoa',
        'pessoa': request.pessoa,
    })


@_login_required
def pessoa_detalhe(request, pk):
    p = get_object_or_404(Pessoa, pk=pk, deletado=False)
    cargos = PessoaCargo.objects.filter(pessoa=p, deletado=False)
    unidades = PessoaUnidade.objects.filter(pessoa=p, deletado=False)
    arquivos = Arquivo.objects.filter(pessoa=p)
    return render(request, 'pessoas/pessoa_detalhe.html', {
        'p': p,
        'cargos': cargos,
        'unidades': unidades,
        'arquivos': arquivos,
        'pessoa': request.pessoa,
    })


@_login_required
@_nivel_required('adm', 'rh')
@transaction.atomic
def pessoa_editar(request, pk):
    p = get_object_or_404(Pessoa, pk=pk, deletado=False)
    dados_antes = {
        'nome': p.nome, 'login': p.login,
        'email': p.email, 'matricula': p.matricula,
    }
    if request.method == 'POST':
        form = PessoaForm(request.POST, instance=p)
        if form.is_valid():
            pessoa = form.save(commit=False)
            senha = form.cleaned_data.get('senha')
            if senha:
                pessoa.senha = make_password(senha)
            pessoa.save()
            _registrar_log(
                request, 'pessoa', p.pk, 'edicao',
                dados_anteriores=dados_antes,
                dados_novos=form.cleaned_data,
            )
            messages.success(request, 'Pessoa atualizada com sucesso.')
            return redirect('pessoas:pessoa_detalhe', pk=p.pk)
    else:
        form = PessoaForm(instance=p)
    return render(request, 'pessoas/pessoa_form.html', {
        'form': form,
        'titulo': f'Editar: {p.nome}',
        'pessoa': request.pessoa,
    })


@_login_required
@_nivel_required('adm', 'rh')
@transaction.atomic
def pessoa_desativar(request, pk):
    p = get_object_or_404(Pessoa, pk=pk)
    if request.method == 'POST':
        p.deletado = True
        p.save()
        _registrar_log(request, 'pessoa', p.pk, 'desativacao')
        messages.success(request, f'{p.nome} desativado(a).')
    return redirect('pessoas:pessoa_lista')


# ── Cargo / Unidade da Pessoa ────────────────────────────────────────

@_login_required
@_nivel_required('adm', 'rh')
def pessoa_cargo_add(request, pk):
    p = get_object_or_404(Pessoa, pk=pk, deletado=False)
    if request.method == 'POST':
        form = PessoaCargoForm(request.POST)
        if form.is_valid():
            pc = form.save(commit=False)
            pc.pessoa = p
            pc.save()
            messages.success(request, 'Cargo atribuído.')
            return redirect('pessoas:pessoa_detalhe', pk=p.pk)
    else:
        form = PessoaCargoForm()
    return render(request, 'pessoas/pessoa_cargo_form.html', {
        'form': form,
        'p': p,
        'pessoa': request.pessoa,
    })


@_login_required
@_nivel_required('adm', 'rh')
def pessoa_unidade_add(request, pk):
    p = get_object_or_404(Pessoa, pk=pk, deletado=False)
    if request.method == 'POST':
        form = PessoaUnidadeForm(request.POST)
        if form.is_valid():
            pu = form.save(commit=False)
            pu.pessoa = p
            pu.save()
            messages.success(request, 'Unidade atribuída.')
            return redirect('pessoas:pessoa_detalhe', pk=p.pk)
    else:
        form = PessoaUnidadeForm()
    return render(request, 'pessoas/pessoa_unidade_form.html', {
        'form': form,
        'p': p,
        'pessoa': request.pessoa,
    })


# ── Agenda / Eventos ─────────────────────────────────────────────────

@_login_required
def agenda(request):
    eventos = Evento.objects.filter(
        Q(geral=True) | Q(pessoa=request.pessoa)
    )
    return render(request, 'pessoas/agenda.html', {
        'eventos': eventos,
        'pessoa': request.pessoa,
    })


@_login_required
def evento_criar(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Evento criado.')
            return redirect('pessoas:agenda')
    else:
        form = EventoForm(
            initial={'pessoa': request.pessoa}
        )
    return render(request, 'pessoas/evento_form.html', {
        'form': form,
        'titulo': 'Novo Evento',
        'pessoa': request.pessoa,
    })


@_login_required
def evento_ferias(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.tipo = 'ferias'
            evento.pessoa = request.pessoa
            evento.save()
            messages.success(request, 'Férias registradas.')
            return redirect('pessoas:agenda')
    else:
        form = EventoForm(initial={
            'tipo': 'ferias',
            'pessoa': request.pessoa,
            'titulo': f'Férias - {request.pessoa.nome}',
        })
    return render(request, 'pessoas/evento_form.html', {
        'form': form,
        'titulo': 'Registrar Férias',
        'pessoa': request.pessoa,
    })


# ── Upload de Arquivos ───────────────────────────────────────────────

@_login_required
@transaction.atomic
def arquivo_upload(request, pk):
    p = get_object_or_404(Pessoa, pk=pk, deletado=False)
    if request.method == 'POST':
        form = ArquivoForm(request.POST, request.FILES)
        if form.is_valid():
            arq = form.save(commit=False)
            arq.pessoa = p
            arq.save()
            _registrar_log(
                request, 'arquivo', arq.pk, 'upload',
                dados_novos=arq.descricao,
            )
            messages.success(request, 'Arquivo enviado.')
            return redirect('pessoas:pessoa_detalhe', pk=p.pk)
    else:
        form = ArquivoForm(initial={'pessoa': p})
    return render(request, 'pessoas/arquivo_form.html', {
        'form': form,
        'p': p,
        'pessoa': request.pessoa,
    })


# ── Dados Estatísticos ───────────────────────────────────────────────

def _estatisticos_visiveis(pessoa):
    dados = DadoEstatistico.objects.select_related('pessoa')
    if pessoa.perfil_acesso not in {'adm', 'rh'}:
        dados = dados.filter(Q(pessoa=pessoa) | Q(pessoa__isnull=True))
    return dados.order_by('-id')


def _links_indicadores(relatorio):
    grupos = [(g['titulo'], g['linhas']) for g in relatorio['grupos']]
    grupos += [
        ('Faixa etária', relatorio['faixas_etarias']),
        ('Tempo de serviço', relatorio['tempo_servico']),
    ]
    rota = reverse('pessoas:estatistico_servidores')
    for titulo, linhas in grupos:
        for indice, linha in enumerate(linhas):
            parametros = {
                'grupo': titulo, 'indice': indice,
                'referencia': relatorio['referencia'].isoformat(),
            }
            linha['url'] = rota + '?' + urlencode(parametros)
            linha['url_acumulado'] = rota + '?' + urlencode({
                **parametros, 'acumulado': '1',
            })
            for genero in ('masculino', 'feminino', 'outros'):
                linha['url_' + genero] = rota + '?' + urlencode({
                    **parametros, 'genero': genero,
                })
            for genero, dados in zip(
                ('masculino', 'feminino'), linha.get('generos', []),
            ):
                dados['url'] = linha['url_' + genero]
                dados['url_acumulado'] = rota + '?' + urlencode({
                    **parametros, 'genero': genero, 'acumulado': '1',
                })


@_login_required
def estatistico_servidores(request):
    try:
        referencia = date.fromisoformat(request.GET.get('referencia', ''))
        indice = int(request.GET.get('indice', ''))
        if request.GET.get('acumulado', '') not in ('', '1'):
            raise ValueError('Acumulado inválido')
        relatorio = relatorio_pessoal(referencia)
        ids, titulo = membros_indicador(
            relatorio, request.GET.get('grupo', ''), indice,
            request.GET.get('genero', ''),
            request.GET.get('acumulado') == '1',
        )
    except (ValueError, TypeError) as erro:
        raise Http404('Indicador ou data de referência inválidos.') from erro
    servidores = Pessoa.objects.filter(
        deletado=False, pk__in=ids,
    ).order_by('nome', 'pk').values('id', 'nome')
    pagina = Paginator(servidores, 50).get_page(request.GET.get('pagina'))
    parametros = request.GET.copy()
    parametros.pop('pagina', None)
    return render(request, 'pessoas/estatistico_servidores.html', {
        'pessoa': request.pessoa, 'pagina': pagina, 'titulo': titulo,
        'referencia': referencia, 'parametros': parametros.urlencode(),
    })


@_login_required
def dado_estatistico_lista(request):
    dados = _estatisticos_visiveis(request.pessoa)
    referencia = timezone.localdate()
    erro_referencia = ''
    if request.GET.get('referencia'):
        try:
            referencia = date.fromisoformat(request.GET['referencia'])
        except ValueError:
            erro_referencia = 'Data inválida. Foi utilizada a data de hoje.'
    relatorio = relatorio_pessoal(referencia)
    if request.GET.get('exportar') == 'csv':
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = (
            'attachment; filename="estatisticas_pessoal.csv"'
        )
        response.write('\ufeff')
        writer = csv.writer(response)
        writer.writerow(['Data de referência', referencia.isoformat()])
        writer.writerow(['Grupo', 'Categoria', 'Total'])
        for grupo in relatorio['grupos']:
            for linha in grupo['linhas']:
                writer.writerow([
                    grupo['titulo'], linha['rotulo'], linha['total'],
                ])
        writer.writerow([
            'Tabela', 'Faixa', 'Masculino', 'Feminino',
            'Outros / não informado', 'Total', '% geral',
            'Acumulado', '% acumulado',
        ])
        for chave, titulo in (
            ('tempo_servico', 'Tempo de serviço'),
            ('faixas_etarias', 'Faixa etária'),
        ):
            for linha in relatorio[chave]:
                writer.writerow([
                    titulo, linha['rotulo'], linha['masculino'],
                    linha['feminino'], linha['outros'], linha['total'],
                    round(linha['percentual'], 2), linha['acumulado'],
                    round(linha['percentual_acumulado'], 2),
                ])
        return response
    _links_indicadores(relatorio)
    return render(request, 'pessoas/dado_estatistico_lista.html', {
        **relatorio,
        'dados': dados,
        'pessoa': request.pessoa,
        'erro_referencia': erro_referencia,
    })


@_login_required
@_nivel_required('adm', 'rh')
def dado_estatistico_criar(request):
    if request.method == 'POST':
        form = DadoEstatisticoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dado estatístico registrado.')
            return redirect('pessoas:dado_estatistico_lista')
    else:
        form = DadoEstatisticoForm()
    return render(request, 'pessoas/dado_estatistico_form.html', {
        'form': form,
        'titulo': 'Novo Dado Estatístico',
        'pessoa': request.pessoa,
    })


# ── Exportações ──────────────────────────────────────────────────────

@_login_required
@_nivel_required('adm', 'rh')
def exportar_pessoas_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = (
        'attachment; filename="pessoas.csv"'
    )
    response.write('\ufeff')
    writer = csv.writer(response)
    writer.writerow([
        'ID', 'Nome', 'Login', 'Matrícula', 'CPF', 'E-mail',
        'Telefone', 'Situação', 'Data Admissão', 'Unidade',
        'Cargo', 'Nível Acesso',
    ])
    pessoas = Pessoa.objects.filter(deletado=False).select_related(
        'id_situacao', 'nivel_acesso',
    )
    for p in pessoas:
        cargo_atual = PessoaCargo.objects.filter(
            pessoa=p, atual=True, deletado=False
        ).select_related('cargo').first()
        unidade_atual = PessoaUnidade.objects.filter(
            pessoa=p, atual=True, deletado=False
        ).select_related('unidade').first()
        writer.writerow([
            p.pk,
            p.nome,
            p.login,
            p.matricula,
            p.cpf,
            p.email,
            p.telefone,
            p.id_situacao.descricao if p.id_situacao else '',
            p.dt_admissao.strftime('%d/%m/%Y') if p.dt_admissao else '',
            str(unidade_atual.unidade) if unidade_atual else '',
            str(cargo_atual.cargo) if cargo_atual else '',
            p.nivel_acesso.descricao if p.nivel_acesso else '',
        ])
    return response


@_login_required
def exportar_estatisticos_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = (
        'attachment; filename="dados_estatisticos.csv"'
    )
    response.write('\ufeff')
    writer = csv.writer(response)
    writer.writerow([
        'ID', 'Pessoa', 'Categoria', 'Indicador',
        'Valor', 'Período', 'Observação',
    ])
    for d in _estatisticos_visiveis(request.pessoa):
        writer.writerow([
            d.pk,
            d.pessoa.nome if d.pessoa else '',
            d.categoria,
            d.indicador,
            d.valor,
            d.periodo,
            d.observacao,
        ])
    return response


# ── Importação CSV ───────────────────────────────────────────────────

@_login_required
@_nivel_required('adm', 'rh')
@transaction.atomic
def importar_pessoas_csv(request):
    if request.method == 'POST':
        form = ImportCSVForm(request.POST, request.FILES)
        if form.is_valid():
            arquivo = request.FILES['arquivo_csv']
            decoded = arquivo.read().decode('utf-8-sig')
            reader = csv.DictReader(io.StringIO(decoded))
            count = 0
            for row in reader:
                Pessoa.objects.create(
                    login=row.get('login', ''),
                    senha=make_password(
                        row.get('senha', 'mudar123')
                    ),
                    nome=row.get('nome', ''),
                    matricula=row.get('matricula', ''),
                    cpf=row.get('cpf', ''),
                    email=row.get('email', ''),
                    telefone=row.get('telefone', ''),
                )
                count += 1
            _registrar_log(
                request, 'pessoa', '-', 'importacao_csv',
                dados_novos=f'{count} registros importados',
            )
            messages.success(
                request, f'{count} pessoa(s) importada(s).'
            )
            return redirect('pessoas:pessoa_lista')
    else:
        form = ImportCSVForm()
    return render(request, 'pessoas/importar_csv.html', {
        'form': form,
        'pessoa': request.pessoa,
    })


# ── Logs de Auditoria ───────────────────────────────────────────────

@_login_required
@_nivel_required('adm')
def log_auditoria(request):
    logs = LogAuditoria.objects.all().order_by('-dt_evento')[:200]
    return render(request, 'pessoas/log_auditoria.html', {
        'logs': logs,
        'pessoa': request.pessoa,
    })
