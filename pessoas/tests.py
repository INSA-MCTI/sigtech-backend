from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from pessoas.models import Evento


class AgendaTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        contas = get_user_model()
        cls.dono = contas.objects.create_user('dono', password='Teste12345!')
        cls.outro = contas.objects.create_user('outro', password='Teste12345!')
        cls.admin = contas.objects.create_user('admin', is_staff=True)
        campos = {
            'tipo': 'F',
            'dt_inicio': timezone.make_aware(datetime(2026, 11, 20, 9)),
            'dt_fim': timezone.make_aware(datetime(2026, 11, 20, 10)),
        }
        cls.privado = Evento.objects.create(
            titulo='Evento privado', criador=cls.dono, **campos,
        )
        cls.geral = Evento.objects.create(
            titulo='Evento geral', criador=cls.dono, geral=True, **campos,
        )
        cls.legado = Evento.objects.create(titulo='Evento antigo', **campos)

    def setUp(self):
        self.client.force_login(self.dono)
        self.dados = {
            'titulo': 'Evento atualizado', 'tipo': 'T',
            'dt_inicio': '2026-11-21T14:30', 'dt_fim': '2026-11-21T15:30',
            'descricao': 'Descrição do evento',
        }

    def test_listagem_visibilidade_e_acoes(self):
        url = reverse('pessoas:agenda_usuario')
        resposta = self.client.get(url)
        self.assertContains(resposta, self.privado.titulo)
        self.assertContains(resposta, reverse(
            'pessoas:editar_evento', args=[self.privado.pk],
        ))
        self.assertContains(resposta, 'container-fluid px-3 px-md-4')
        self.client.force_login(self.outro)
        resposta = self.client.get(url)
        self.assertContains(resposta, self.geral.titulo)
        self.assertNotContains(resposta, self.privado.titulo)
        self.assertNotContains(resposta, self.legado.titulo)
        self.assertNotContains(resposta, reverse(
            'pessoas:excluir_evento', args=[self.geral.pk],
        ))

    def test_cadastro_vincula_criador_e_redireciona_para_agenda(self):
        resposta = self.client.post(
            reverse('pessoas:criar_evento'), self.dados,
        )
        self.assertRedirects(resposta, reverse('pessoas:agenda_usuario'))
        self.assertEqual(
            Evento.objects.get(titulo=self.dados['titulo']).criador,
            self.dono,
        )

    def test_edicao_exibe_datas_e_preserva_criador(self):
        url = reverse('pessoas:editar_evento', args=[self.privado.pk])
        resposta = self.client.get(url)
        self.assertContains(resposta, 'value="2026-11-20T09:00"')
        resposta = self.client.post(url, self.dados)
        self.assertRedirects(resposta, reverse('pessoas:agenda_usuario'))
        self.privado.refresh_from_db()
        self.assertEqual(self.privado.titulo, self.dados['titulo'])
        self.assertEqual(self.privado.criador, self.dono)

    def test_formulario_invalido_mantem_dados_e_nao_salva(self):
        dados = {**self.dados, 'dt_fim': '2026-11-20T09:00'}
        resposta = self.client.post(
            reverse('pessoas:editar_evento', args=[self.privado.pk]), dados,
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'não pode ser anterior')
        self.assertContains(resposta, 'Evento atualizado')
        self.privado.refresh_from_db()
        self.assertEqual(self.privado.titulo, 'Evento privado')

    def test_exclusao_exige_post_e_csrf(self):
        url = reverse('pessoas:excluir_evento', args=[self.privado.pk])
        self.assertEqual(self.client.get(url).status_code, 405)
        protegido = Client(enforce_csrf_checks=True)
        protegido.force_login(self.dono)
        self.assertEqual(protegido.post(url).status_code, 403)
        self.assertTrue(Evento.objects.filter(pk=self.privado.pk).exists())
        self.assertRedirects(
            self.client.post(url), reverse('pessoas:agenda_usuario'),
        )
        self.assertFalse(Evento.objects.filter(pk=self.privado.pk).exists())

    def test_outro_usuario_nao_pode_alterar_ou_excluir(self):
        self.client.force_login(self.outro)
        for evento, esperado in ((self.geral, 403), (self.privado, 404)):
            for rota in ('editar_evento', 'excluir_evento'):
                resposta = self.client.post(
                    reverse('pessoas:' + rota, args=[evento.pk]), self.dados,
                )
                self.assertEqual(resposta.status_code, esperado)
        self.assertTrue(Evento.objects.filter(pk=self.geral.pk).exists())

    def test_administrador_gerencia_eventos_anteriores(self):
        self.client.force_login(self.admin)
        resposta = self.client.get(reverse('pessoas:agenda_usuario'))
        self.assertContains(resposta, self.legado.titulo)
        resposta = self.client.post(
            reverse('pessoas:editar_evento', args=[self.legado.pk]),
            self.dados,
        )
        self.assertRedirects(resposta, reverse('pessoas:agenda_usuario'))

    def test_exige_login_e_login_redireciona_para_agenda(self):
        self.client.logout()
        resposta = self.client.get(reverse('pessoas:agenda_usuario'))
        self.assertEqual(resposta.status_code, 302)
        self.assertIn(reverse('pessoas:login'), resposta.url)
        resposta = self.client.post(
            reverse('pessoas:login'),
            {'login': 'dono', 'senha': 'Teste12345!'},
        )
        self.assertRedirects(resposta, reverse('pessoas:agenda_usuario'))
