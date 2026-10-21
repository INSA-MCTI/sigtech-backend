import json
from datetime import date
from types import SimpleNamespace
from unittest.mock import patch

from django.test import SimpleTestCase

from pessoas.estatisticas import anos_completos, distribuicao, tabela_faixas
from pessoas.forms import PessoaForm
from pessoas.models import NivelAcesso, Pessoa, Situacao
from pessoas.views import (
    _estatisticos_visiveis,
    _registrar_log,
    _serializar_auditoria,
)


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
