from django.db import models

from core.models import EntidadeBase


class Contrato(EntidadeBase):
    """
    Modelo que representa um contrato.
    """

    class ContratoStatus(models.IntegerChoices):
        VIGENTE = 1, 'Vigente'
        ENCERRADO = 2, 'Encerrado'
        SUSPENSO = 3, 'Suspenso'

    # 1. Todos os campos do banco DEVEM ficar no escopo da classe
    codigo = models.CharField(max_length=100, unique=True)
    numero_do_processo = models.CharField(max_length=100, unique=True)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    numero_de_parcelas = models.IntegerField()
    valor_da_parcela = models.DecimalField(max_digits=10, decimal_places=2)

    # Dica: Substitua IntegerField por models.ForeignKey se esses
    # IDs referenciarem Usuários/Gestores
    id_gestor = models.IntegerField()
    id_gestor_substituto = models.IntegerField()
    id_fiscal = models.IntegerField()
    id_fiscal_substituto = models.IntegerField()

    status = models.IntegerField(
        choices=ContratoStatus.choices, default=ContratoStatus.VIGENTE
    )

    @property
    def is_vigente(self):
        """Retorna True se o contrato estiver vigente, 
        caso contrário, retorna False."""
        return self.status == self.ContratoStatus.VIGENTE

    @property
    def is_encerrado(self):
        """Retorna True se o contrato estiver encerrado, 
        caso contrário, retorna False."""
        return self.status == self.ContratoStatus.ENCERRADO

    @property
    def data_fim(self):
        """
        Retorna a data de fim do contrato formatada como string no 
        formato 'dd/mm/yyyy'."""
        return self.data_fim.strftime('%d/%m/%Y')

    @property
    def data_inicio(self):
        """
        Retorna a data de início do contrato formatada como string no 
        formato 'dd/mm/yyyy'.
        """
        return self.data_inicio.strftime('%d/%m/%Y')
