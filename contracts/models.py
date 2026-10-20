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

    codigo = models.CharField(max_length=100, unique=True)
    # Unique=True se um processo só gera um contrato
    numero_do_processo = models.CharField(max_length=100, unique=True)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    valor_total = models.DecimalField(max_digits=14, decimal_places=2)
    numero_de_parcelas = models.PositiveIntegerField()
    valor_da_parcela = models.DecimalField(max_digits=14, decimal_places=2)
    objeto = models.CharField(max_length=255)

    id_gestor = models.PositiveIntegerField(db_index=True)
    id_gestor_substituto = models.PositiveIntegerField(db_index=True)
    id_fiscal = models.PositiveIntegerField(db_index=True)
    id_fiscal_substituto = models.PositiveIntegerField(db_index=True)

    status = models.IntegerField(
        choices=ContratoStatus.choices, default=ContratoStatus.VIGENTE
    )

    class Meta:
        # Restrições de Registro na Tabela de Contratos
        constraints = [
            models.CheckConstraint(
                condition=models.Q(data_fim__gte=models.F('data_inicio')),
                name='datas_fim_maior_ou_igual_data_inicio',
            ),
            models.CheckConstraint(
                condition=models.Q(valor_total__gte=0)
                & models.Q(valor_da_parcela__gte=0),
                name='contrato_valores_nao_negativos',
            ),
        ]

    def __str__(self):
        return f'Contrato {self.codigo} - {self.objeto}'

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
    def data_fim_formatada(self):
        """
        Retorna a data de fim do contrato formatada como string no
        formato 'dd/mm/yyyy'."""
        return self.data_fim.strftime('%d/%m/%Y')

    @property
    def data_inicio_formatada(self):
        """
        Retorna a data de início do contrato formatada como string no
        formato 'dd/mm/yyyy'.
        """
        return self.data_inicio.strftime('%d/%m/%Y')
