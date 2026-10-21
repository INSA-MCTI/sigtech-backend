from django.contrib import admin

from .models import (
    Arquivo,
    Cargo,
    Carreira,
    DadoEstatistico,
    Evento,
    LogAuditoria,
    NivelAcesso,
    Pessoa,
    PessoaCargo,
    PessoaSituacaoHistorico,
    PessoaUnidade,
    Situacao,
    Unidade,
)


class PessoaCargoInline(admin.TabularInline):
    model = PessoaCargo
    extra = 1


class PessoaUnidadeInline(admin.TabularInline):
    model = PessoaUnidade
    extra = 1


@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = [
        'nome',
        'login',
        'matricula',
        'cpf',
        'email',
        'id_situacao',
        'deletado',
    ]
    list_filter = ['id_situacao', 'nivel_acesso', 'deletado']
    search_fields = ['nome', 'login', 'matricula', 'cpf', 'email']
    inlines = [PessoaCargoInline, PessoaUnidadeInline]


@admin.register(NivelAcesso)
class NivelAcessoAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'deletado']


@admin.register(Situacao)
class SituacaoAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'deletado']


@admin.register(Carreira)
class CarreiraAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'deletado']


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'nivel', 'siape', 'cargo', 'deletado']


@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ['sigla', 'descricao', 'unidade_superior', 'deletado']


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'dt_inicio', 'dt_fim', 'pessoa', 'geral']
    list_filter = ['tipo', 'geral']


@admin.register(Arquivo)
class ArquivoAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'tipo', 'pessoa', 'arquivo']


@admin.register(DadoEstatistico)
class DadoEstatisticoAdmin(admin.ModelAdmin):
    list_display = [
        'categoria',
        'indicador',
        'valor',
        'periodo',
        'pessoa',
    ]


@admin.register(LogAuditoria)
class LogAuditoriaAdmin(admin.ModelAdmin):
    list_display = ['tabela', 'acao', 'pessoa', 'dt_evento', 'ip']
    list_filter = ['tabela', 'acao']
    readonly_fields = [
        'pessoa',
        'tabela',
        'id_registro',
        'acao',
        'dados_anteriores',
        'dados_novos',
        'ip',
        'dt_evento',
    ]


@admin.register(PessoaSituacaoHistorico)
class PessoaSituacaoHistoricoAdmin(admin.ModelAdmin):
    list_display = [
        'pessoa',
        'situacao_anterior',
        'situacao_nova',
        'dt_alteracao',
    ]
