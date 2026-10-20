from django.db import models


class EntidadeBase(models.Model):
    """
    Modelo base para todas as entidades do sistema.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # indica que o Django não vai criar uma tabela para este modelo
        abstract = True
