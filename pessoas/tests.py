import json
from datetime import date
from types import SimpleNamespace
from unittest.mock import patch

from django import forms
from django.core.exceptions import ValidationError
from django.http import Http404
from django.test import RequestFactory, SimpleTestCase, override_settings

from pessoas.estatisticas import (
    anos_completos, distribuicao, membros_indicador, tabela_faixas,
)
from pessoas.forms import PessoaCargoForm, PessoaForm, PessoaUnidadeForm
from pessoas.models import (
    Cargo, NivelAcesso, Pessoa, PessoaCargo, PessoaUnidade, Situacao,
)
from pessoas.views import (
    _estatisticos_visiveis,
    _registrar_log,
    _serializar_auditoria,
    estatistico_servidores,
    exportar_pessoas_csv,
)


class ExportacaoPessoasTests(SimpleTestCase):
    def test_consulta_de_cargo_usa_coluna_siape(self):
        sql = str(PessoaCargo.objects.select_related('cargo').query)
        self.assertIn('`cargo`.`siape`', sql)
        self.assertNotIn('`cargo`.`classe`', sql)
        self.assertEqual(Cargo._meta.get_field('siape').column, 'siape')

    @patch('pessoas.views.PessoaUnidade.objects.filter')
    @patch('pessoas.views.PessoaCargo.objects.filter')
    @patch('pessoas.views.Pessoa.objects.filter')
    @patch('pessoas.views._get_pessoa_logada')
    def test_exportacao_com_cargo_e_unidade(
        self, logada, pessoas, cargos, unidades,
    ):
        logada.return_value = Pessoa(
            pk=1, nivel_acesso=NivelAcesso(descricao='Administrador'),
        )
        pessoas.return_value.select_related.return_value = [
            Pessoa(
                pk=2, nome='Servidor de teste', login='servidor',
                dt_admissao=date(2020, 1, 2),
            ),
        ]
        cargos.return_value.select_related.return_value.first.return_value = (
            SimpleNamespace(cargo=Cargo(descricao='Analista', siape='123'))
        )
        unidades.return_value.select_related.return_value.first.return_value = (
            SimpleNamespace(unidade='RH - Recursos Humanos')
        )
        response = exportar_pessoas_csv(RequestFactory().get('/'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('pessoas.csv', response['Content-Disposition'])
        self.assertContains(response, 'Analista')
        self.assertContains(response, '02/01/2020')
        self.assertContains(response, 'RH - Recursos Humanos')
        self.assertNotIn('senha', response.content.decode('utf-8').lower())


class PessoaDropdownTests(SimpleTestCase):
    def test_opcoes_e_widgets_do_cadastro(self):
        form = PessoaForm()
        opcoes = {
            'genero': ['M', 'F'],
            'titulacao': [
                'Técnico', 'Graduação', 'Especialização', 'Mestrado',
                'Doutorado', 'Pós-doutorado', 'não possui',
            ],
            'escolaridade': [
                'Ensino Fundamental', 'Ensino Médio', 'Ensino Superior',
            ],
        }
        for nome, valores in opcoes.items():
            campo = form.fields[nome]
            self.assertIsInstance(campo.widget, forms.Select)
            self.assertEqual(
                [valor for valor, _ in campo.choices if valor], valores,
            )
            for valor in valores:
                self.assertEqual(campo.clean(valor), valor)
            with self.assertRaises(ValidationError):
                campo.clean('opcao-invalida')

    def test_edicao_mantem_opcoes_selecionadas(self):
        form = PessoaForm(instance=Pessoa(
            pk=1, genero='F', titulacao='Doutorado',
            escolaridade='Ensino Superior',
        ))
        self.assertEqual(form['genero'].value(), 'F')
        self.assertEqual(form['titulacao'].value(), 'Doutorado')
        self.assertEqual(form['escolaridade'].value(), 'Ensino Superior')


@override_settings(LANGUAGE_CODE='pt-br')
class DatasFormTests(SimpleTestCase):
    def test_datas_existentes_renderizadas_em_iso(self):
        data = date(2026, 10, 21)
        casos = [
            (PessoaForm(instance=Pessoa(
                pk=1, dt_nascimento=data, dt_admissao=data, dt_demissao=data,
            )), ['dt_nascimento', 'dt_admissao', 'dt_demissao']),
            (PessoaCargoForm(instance=PessoaCargo(
                pk=1, dt_inicio=data, dt_fim=data,
            )), ['dt_inicio', 'dt_fim']),
            (PessoaUnidadeForm(instance=PessoaUnidade(
                pk=1, dt_inicio=data, dt_fim=data,
            )), ['dt_inicio', 'dt_fim']),
        ]
        for form, campos in casos:
            for campo in campos:
                with self.subTest(form=type(form).__name__, campo=campo):
                    html = str(form[campo])
                    self.assertIn('type="date"', html)
                    self.assertIn('value="2026-10-21"', html)
                    self.assertEqual(
                        form.fields[campo].clean('2026-10-21'), data,
                    )

    def test_datas_ausentes_continuam_vazias(self):
        form = PessoaForm(instance=Pessoa(pk=1))
        for campo in ('dt_nascimento', 'dt_admissao', 'dt_demissao'):
            self.assertNotIn('value=', str(form[campo]))
            self.assertIsNone(form.fields[campo].clean(''))

    def test_data_enviada_permanece_apos_erro_de_validacao(self):
        form = PessoaForm(data={'dt_nascimento': '1990-03-15'})
        self.assertIn('value="1990-03-15"', str(form['dt_nascimento']))


class SenhaFormTests(SimpleTestCase):
    def test_edicao_nao_sobrescreve_hash_com_senha_vazia(self):
        pessoa = Pessoa(pk=1, senha='hash-existente')
        form = PessoaForm(instance=pessoa)
        form.cleaned_data = {'senha': ''}
        with patch.object(form, '_get_validation_exclusions', return_value=[]):
            with patch.object(pessoa, 'full_clean'):
                with patch.object(form, 'validate_unique'):
                    form._post_clean()
        self.assertEqual(pessoa.senha, 'hash-existente')
        self.assertFalse(form.fields['senha'].required)

    def test_cadastro_exige_senha(self):
        self.assertTrue(PessoaForm().fields['senha'].required)


class AuditoriaTests(SimpleTestCase):
    def test_dados_ausentes_sao_nulos(self):
        self.assertIsNone(_serializar_auditoria(None))
        self.assertIsNone(_serializar_auditoria(''))

    def test_serializa_datas_relacoes_e_remove_senha(self):
        dados = {
            'nome': 'Pessoa de teste',
            'senha': 'nao deve aparecer',
            'password': 'tambem nao',
            'dt_admissao': date(2026, 10, 21),
            'id_situacao': Situacao(pk=1),
        }
        resultado = json.loads(_serializar_auditoria(dados))
        self.assertEqual(resultado['dt_admissao'], '2026-10-21')
        self.assertEqual(resultado['id_situacao'], 1)
        self.assertNotIn('senha', resultado)
        self.assertNotIn('password', resultado)

    def test_texto_simples_tambem_e_json_valido(self):
        self.assertEqual(
            json.loads(_serializar_auditoria('Certificado')),
            'Certificado',
        )

    @patch('pessoas.views.LogAuditoria.objects.create')
    def test_log_respeita_limite_da_acao_e_dados_nulos(self, criar):
        request = SimpleNamespace(META={'REMOTE_ADDR': '127.0.0.1'})
        for acao, esperado in (
            ('desativacao', 'desativar'),
            ('importacao_csv', 'importar'),
        ):
            _registrar_log(request, 'pessoa', 1, acao)
            self.assertEqual(criar.call_args.kwargs['acao'], esperado)
            self.assertIsNone(
                criar.call_args.kwargs['dados_anteriores']
            )


class EstatisticosTests(SimpleTestCase):
    @patch('pessoas.views.DadoEstatistico.objects.select_related')
    def test_administrador_consulta_todos_os_dados(self, consultar):
        pessoa = Pessoa(
            pk=1, nivel_acesso=NivelAcesso(descricao='Administrador')
        )
        _estatisticos_visiveis(pessoa)
        consultar.return_value.filter.assert_not_called()
        consultar.return_value.order_by.assert_called_once_with('-id')

    @patch('pessoas.views.DadoEstatistico.objects.select_related')
    def test_servidor_consulta_apenas_dados_proprios_e_gerais(self, consultar):
        pessoa = Pessoa(
            pk=2, nivel_acesso=NivelAcesso(descricao='Servidor')
        )
        _estatisticos_visiveis(pessoa)
        filtro = consultar.return_value.filter.call_args.args[0]
        self.assertEqual(filtro.connector, 'OR')
        self.assertEqual(
            filtro.children, [('pessoa', pessoa), ('pessoa__isnull', True)]
        )
        consultar.return_value.filter.return_value.order_by.assert_called_once_with(
            '-id'
        )


class RelatorioPessoalTests(SimpleTestCase):
    def test_anos_completos_respeitam_aniversario(self):
        referencia = date(2026, 10, 21)
        self.assertEqual(anos_completos(date(1996, 10, 21), referencia), 30)
        self.assertEqual(anos_completos(date(1996, 10, 22), referencia), 29)
        self.assertIsNone(anos_completos(date(2027, 1, 1), referencia))
        self.assertIsNone(anos_completos(None, referencia))

    def test_faixas_incluem_genero_e_datas_ausentes(self):
        registros = [
            {'genero': 'm', 'data': date(1996, 10, 21)},
            {'genero': 'F', 'data': date(1995, 10, 21)},
            {'genero': None, 'data': None},
        ]
        linhas, media = tabela_faixas(
            registros, 'data', date(2026, 10, 21),
            [('Até 30', 30), ('Acima de 30', None)],
        )
        self.assertEqual([linha['total'] for linha in linhas], [1, 1, 1])
        self.assertEqual(linhas[0]['masculino'], 1)
        self.assertEqual(linhas[1]['feminino'], 1)
        self.assertEqual(linhas[2]['outros'], 1)
        self.assertEqual(linhas[-1]['percentual_acumulado'], 100)
        self.assertEqual(media, 30.5)

    def test_relatorio_vazio_nao_divide_por_zero(self):
        linhas, media = tabela_faixas(
            [], 'data', date(2026, 10, 21), [('Todas', None)],
        )
        self.assertIsNone(media)
        self.assertTrue(all(linha['percentual'] == 0 for linha in linhas))

    def test_distribuicao_agrupa_campos_vazios(self):
        self.assertEqual(distribuicao([None, '', '  ']), [
            {'rotulo': 'Não informado', 'total': 3},
        ])


class ServidoresIndicadorTests(SimpleTestCase):
    def setUp(self):
        faixas, _ = tabela_faixas([
            {'id': 1, 'genero': 'M', 'data': date(2000, 1, 1)},
            {'id': 2, 'genero': 'F', 'data': date(1980, 1, 1)},
            {'id': 3, 'genero': None, 'data': None},
        ], 'data', date(2026, 10, 21), [('Até 30', 30), ('Acima', None)])
        self.relatorio = {
            'grupos': [{
                'titulo': 'Titulação',
                'linhas': distribuicao(
                    [' Doutorado ', 'Doutorado', None], [1, 2, 3],
                ),
            }],
            'faixas_etarias': faixas, 'tempo_servico': faixas,
            'referencia': date(2026, 10, 21),
        }

    def test_categoria_e_campos_ausentes_coincidem_com_contagem(self):
        for indice, linha in enumerate(self.relatorio['grupos'][0]['linhas']):
            ids, _ = membros_indicador(self.relatorio, 'Titulação', indice)
            self.assertEqual(len(ids), linha['total'])
        self.assertEqual(
            membros_indicador(self.relatorio, 'Titulação', 0)[0], {1, 2},
        )

    def test_faixas_genero_e_acumulados(self):
        self.assertEqual(membros_indicador(
            self.relatorio, 'Faixa etária', 1, 'feminino',
        )[0], {2})
        self.assertEqual(membros_indicador(
            self.relatorio, 'Faixa etária', 1, acumulado=True,
        )[0], {1, 2})
        self.assertEqual(membros_indicador(
            self.relatorio, 'Faixa etária', 2, 'outros',
        )[0], {3})

    def test_rejeita_filtros_nao_previstos(self):
        for grupo, indice, genero in (
            ('senha', 0, ''), ('Titulação', -1, ''),
            ('Titulação', 99, ''), ('Titulação', 0, 'masculino'),
            ('Faixa etária', 0, 'invalido'),
        ):
            with self.assertRaises(ValueError):
                membros_indicador(self.relatorio, grupo, indice, genero)

    @patch('pessoas.views.Pessoa.objects.filter')
    @patch('pessoas.views.relatorio_pessoal')
    @patch('pessoas.views._get_pessoa_logada')
    def test_servidor_acessa_lista_sem_dados_pessoais(
        self, logada, relatorio, filtrar,
    ):
        logada.return_value = Pessoa(
            pk=2, nivel_acesso=NivelAcesso(descricao='Servidor'),
        )
        relatorio.return_value = self.relatorio
        filtrar.return_value.order_by.return_value.values.return_value = [
            {'id': 1, 'nome': 'Servidor A'}, {'id': 2, 'nome': 'Servidor B'},
        ]
        request = RequestFactory().get('/pessoas/estatisticos/servidores/', {
            'referencia': '2026-10-21', 'grupo': 'Titulação', 'indice': '0',
        })
        response = estatistico_servidores(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Servidor A')
        filtrar.assert_called_once_with(deletado=False, pk__in={1, 2})
        filtrar.return_value.order_by.return_value.values.assert_called_once_with(
            'id', 'nome',
        )

    @patch('pessoas.views._get_pessoa_logada', return_value=None)
    def test_exige_login(self, logada):
        response = estatistico_servidores(RequestFactory().get('/'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/pessoas/login/')

    @patch('pessoas.views._get_pessoa_logada', return_value=Pessoa(pk=1))
    def test_data_invalida_nao_altera_silenciosamente_o_filtro(self, logada):
        request = RequestFactory().get('/', {'referencia': 'invalida'})
        with self.assertRaises(Http404):
            estatistico_servidores(request)
