from django.conf import settings
from django.db import models

from core.models import EntidadeBase

# Create your models here.


class Contato(EntidadeBase):
    """
    Modelo que representa um contato. Cria a
    tabela contatos e coloca como FK a tabela Pessoa
    """

    pessoa = models.ForeignKey(
        'Pessoa', on_delete=models.CASCADE, related_name='contatos'
    )
    telefone = models.CharField(max_length=15)
    ramal = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(unique=True)


class SituacaoVinculoEnum(models.TextChoices):
    """
    Enumeração para representar a situação do vínculo de uma pessoa.
    """

    ATIVO = 'A', 'Ativo'
    INATIVO = 'I', 'Inativo'
    LICENCA = 'S', 'Licenca'


class Vinculo(EntidadeBase):
    """
    Modelo que representa o vínculo de uma pessoa.
    Enumeração para representar o vínculo de trabalho de uma pessoa.
    """

    class VinculoTrabalhoEnum(models.TextChoices):
        ESTAGIARIO = 'E', 'Estagiário'
        TERCEIRIZADO = 'T', 'Terceirizado'
        SERVIDOR = 'S', 'Servidor'

    pessoa = models.ForeignKey(
        'Pessoa', on_delete=models.CASCADE, related_name='vinculos'
    )
    tipo_vinculo = models.CharField(
        max_length=1, choices=VinculoTrabalhoEnum.choices
    )
    situacao = models.CharField(
        max_length=1, choices=SituacaoVinculoEnum.choices
    )
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)


class TitulacaoEnum(models.TextChoices):
    """
    Enumeração para representar a titulação de uma pessoa.
    """

    TECNICO = 'T', 'Técnico'
    ESPECIALIZACAO = 'E', 'Especialização'
    MESTRADO = 'M', 'Mestrado'
    DOUTORADO = 'D', 'Doutorado'


class EscolaridadeEnum(models.TextChoices):
    """
    Enumeração para representar a escolaridade de uma pessoa.
    """

    ENSINO_FUNDAMENTAL_COMPLETO = 'F', 'Fundamental Completo'
    ENSINO_MEDIO_COMPLETO = 'M', 'Médio Completo'
    ENSINO_SUPERIOR_COMPLETO = 'S', 'Superior'
    OUTROS = 'O', 'Outros'


class Endereco(EntidadeBase):
    """
    Modelo que representa um endereço.
    """

    pessoa = models.ForeignKey(
        'Pessoa',
        on_delete=models.CASCADE,
        related_name='enderecos',
    )
    cep = models.CharField(max_length=8)
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=255, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)


class Formacao(EntidadeBase):
    """
    Modelo que representa a formação acadêmica de uma pessoa.
    """

    pessoa = models.ForeignKey(
        'Pessoa',
        on_delete=models.CASCADE,
        related_name='formacoes',
    )
    escolaridade = models.CharField(
        max_length=1, choices=EscolaridadeEnum.choices
    )
    titulacao = models.CharField(max_length=1, choices=TitulacaoEnum.choices)


class SexoEnum(models.TextChoices):
    """
    Enumeração para representar o sexo de uma pessoa.
    """

    MASCULINO = 'M', 'Masculino'
    FEMININO = 'F', 'Feminino'
    OUTRO = 'O', 'Outro'


class Usuario(EntidadeBase):
    """
    Modelo que representa um usuário do sistema.
    """

    pessoa = models.OneToOneField(
        'Pessoa',
        on_delete=models.CASCADE,
        related_name='usuario',
    )

    # Permite que cada perfil no sistema tenha uma conta de autenticação
    # associada
    conta = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil_usuario',
    )


class Pessoa(EntidadeBase):
    """
    Modelo que representa uma pessoa.
    """

    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11, unique=True)
    data_nascimento = models.DateField()
    genero = models.CharField(
        max_length=1, choices=SexoEnum.choices, default=SexoEnum.OUTRO
    )
