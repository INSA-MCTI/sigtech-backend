from django.db import models


# ── Tabelas legadas (managed = False) ───────────────────────────────


class NivelAcesso(models.Model):
    id = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=100)
    deletado = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'nivel_acesso'
        verbose_name = 'Nível de Acesso'
        verbose_name_plural = 'Níveis de Acesso'

    def __str__(self):
        return self.descricao


class Situacao(models.Model):
    id = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=200)
    deletado = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'situacao'
        verbose_name = 'Situação'
        verbose_name_plural = 'Situações'

    def __str__(self):
        return self.descricao


class Carreira(models.Model):
    id = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=200)
    deletado = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'carreira'

    def __str__(self):
        return self.descricao


class Cargo(models.Model):
    id = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=200)
    nivel = models.CharField(max_length=50, blank=True)
    siape = models.CharField(max_length=50, blank=True)
    cargo = models.CharField(max_length=200, blank=True)
    padrao = models.CharField(max_length=50, blank=True)
    deletado = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'cargo'

    def __str__(self):
        return self.descricao


class Unidade(models.Model):
    id = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=200)
    sigla = models.CharField(max_length=20)
    unidade_superior = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subunidades',
        db_column='id_unidade_superior',
    )
    deletado = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'unidade'

    def __str__(self):
        return f'{self.sigla} - {self.descricao}'


class Pessoa(models.Model):
    id = models.AutoField(primary_key=True)
    login = models.CharField(max_length=100, unique=True)
    senha = models.CharField(max_length=100)
    nome = models.CharField(max_length=100)
    dt_nascimento = models.DateField(
        null=True, blank=True, verbose_name='Data de Nascimento'
    )
    dt_admissao = models.DateField(
        null=True, blank=True, verbose_name='Data de Admissão'
    )
    dt_demissao = models.DateField(
        null=True, blank=True, verbose_name='Data de Demissão'
    )
    matricula = models.CharField(max_length=50, blank=True, null=True)
    cpf = models.CharField(
        max_length=15, verbose_name='CPF'
    )
    id_situacao = models.ForeignKey(
        Situacao,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_situacao',
        verbose_name='Situação',
    )
    id_carreira = models.ForeignKey(
        Carreira,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_carreira',
        verbose_name='Carreira',
    )
    escolaridade = models.CharField(
        max_length=100, blank=True, null=True
    )
    titulacao = models.CharField(
        max_length=100, blank=True, null=True
    )
    id_responsavel = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subordinados',
        db_column='id_responsavel',
    )
    cep = models.CharField(
        max_length=10, blank=True, null=True, verbose_name='CEP'
    )
    logradouro = models.CharField(
        max_length=100, blank=True, null=True
    )
    complemento = models.CharField(
        max_length=100, blank=True, null=True
    )
    bairro = models.CharField(
        max_length=100, blank=True, null=True
    )
    cidade = models.CharField(
        max_length=100, blank=True, null=True
    )
    estado = models.CharField(max_length=3, blank=True, null=True)
    telefone = models.CharField(
        max_length=15, blank=True, null=True
    )
    email = models.CharField(
        max_length=100, blank=True, null=True
    )
    genero = models.CharField(max_length=1, blank=True, null=True)
    nivel_acesso = models.ForeignKey(
        NivelAcesso,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='nivel_acesso',
    )
    deletado = models.BooleanField(default=False)
    dt_criacao = models.DateTimeField(auto_now_add=True)
    dt_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'pessoa'

    @property
    def perfil_acesso(self):
        if not self.nivel_acesso or self.nivel_acesso.deletado:
            return ''
        descricao = self.nivel_acesso.descricao.strip().lower()
        return 'adm' if descricao == 'administrador' else descricao

    def __str__(self):
        return self.nome


class PessoaCargo(models.Model):
    id = models.AutoField(primary_key=True)
    pessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.CASCADE,
        related_name='cargos',
        db_column='id_pessoa',
    )
    cargo = models.ForeignKey(
        Cargo,
        on_delete=models.CASCADE,
        db_column='id_cargo',
    )
    dt_inicio = models.DateField(null=True, blank=True)
    dt_fim = models.DateField(null=True, blank=True)
    atual = models.BooleanField(default=True)
    deletado = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'pessoa_cargo'
        verbose_name = 'Cargo da Pessoa'
        verbose_name_plural = 'Cargos da Pessoa'

    def __str__(self):
        return f'{self.pessoa} - {self.cargo}'


class PessoaUnidade(models.Model):
    id = models.AutoField(primary_key=True)
    pessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.CASCADE,
        related_name='unidades',
        db_column='id_pessoa',
    )
    unidade = models.ForeignKey(
        Unidade,
        on_delete=models.CASCADE,
        db_column='id_unidade',
    )
    dt_inicio = models.DateField(null=True, blank=True)
    dt_fim = models.DateField(null=True, blank=True)
    chefia = models.BooleanField(default=False)
    atual = models.BooleanField(default=True)
    deletado = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'pessoa_unidade'
        verbose_name = 'Unidade da Pessoa'
        verbose_name_plural = 'Unidades da Pessoa'

    def __str__(self):
        return f'{self.pessoa} - {self.unidade}'


class PessoaSituacaoHistorico(models.Model):
    id = models.AutoField(primary_key=True)
    pessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.CASCADE,
        related_name='historico_situacoes',
        db_column='id_pessoa',
    )
    situacao_anterior = models.ForeignKey(
        Situacao,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='historicos_anterior',
        db_column='id_situacao_anterior',
    )
    situacao_nova = models.ForeignKey(
        Situacao,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='historicos_nova',
        db_column='id_situacao_nova',
    )
    dt_alteracao = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'pessoa_situacao_historico'
        verbose_name = 'Histórico de Situação'
        verbose_name_plural = 'Históricos de Situação'

    def __str__(self):
        return f'{self.pessoa} - {self.situacao_nova}'


class LogAuditoria(models.Model):
    id = models.AutoField(primary_key=True)
    pessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_pessoa',
    )
    tabela = models.CharField(max_length=100)
    id_registro = models.CharField(max_length=100)
    acao = models.CharField(max_length=50)
    dados_anteriores = models.TextField(blank=True, null=True)
    dados_novos = models.TextField(blank=True, null=True)
    ip = models.CharField(max_length=45, null=True, blank=True)
    dt_evento = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'log_auditoria'
        verbose_name = 'Log de Auditoria'
        verbose_name_plural = 'Logs de Auditoria'

    def __str__(self):
        return f'{self.tabela} - {self.acao} - {self.dt_evento}'


# ── Tabelas novas (managed = True) ──────────────────────────────────


class Evento(models.Model):
    id = models.AutoField(primary_key=True)

    TIPO_CHOICES = [
        ('ferias', 'Férias'),
        ('evento', 'Evento'),
        ('reuniao', 'Reunião'),
        ('treinamento', 'Treinamento'),
        ('outro', 'Outro'),
    ]

    titulo = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, default='')
    dt_inicio = models.DateTimeField()
    dt_fim = models.DateTimeField()
    tipo = models.CharField(
        max_length=20, choices=TIPO_CHOICES, default='evento'
    )
    pessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.CASCADE,
        related_name='eventos',
        db_column='id_pessoa',
        null=True,
        blank=True,
    )
    geral = models.BooleanField(
        default=False,
        help_text='Evento visível para todos',
    )

    class Meta:
        db_table = 'evento'
        ordering = ['-dt_inicio']

    def __str__(self):
        return self.titulo


class Arquivo(models.Model):
    id = models.AutoField(primary_key=True)

    TIPO_CHOICES = [
        ('certificado', 'Certificado'),
        ('justificativa', 'Justificativa'),
        ('documento', 'Documento'),
        ('outro', 'Outro'),
    ]

    pessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.CASCADE,
        related_name='arquivos',
        db_column='id_pessoa',
    )
    tipo = models.CharField(
        max_length=20, choices=TIPO_CHOICES, default='documento'
    )
    descricao = models.CharField(max_length=255)
    arquivo = models.FileField(upload_to='uploads/%Y/%m/')

    class Meta:
        db_table = 'arquivo'

    def __str__(self):
        return f'{self.descricao} ({self.pessoa})'


class DadoEstatistico(models.Model):
    id = models.AutoField(primary_key=True)
    pessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.CASCADE,
        related_name='dados_estatisticos',
        db_column='id_pessoa',
        null=True,
        blank=True,
    )
    categoria = models.CharField(max_length=100)
    indicador = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    periodo = models.CharField(max_length=50, blank=True, default='')
    observacao = models.TextField(blank=True, default='')

    class Meta:
        db_table = 'dado_estatistico'
        verbose_name = 'Dado Estatístico'
        verbose_name_plural = 'Dados Estatísticos'

    def __str__(self):
        return f'{self.categoria} - {self.indicador}: {self.valor}'
