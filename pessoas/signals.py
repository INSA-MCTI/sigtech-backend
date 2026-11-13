from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Usuario

@receiver(post_delete, sender=Usuario)
def deletar_pessoa_ao_apagar_user(sender, instance, **kwargs):
    if getattr(instance, 'pessoa', None):
        instance.pessoa.delete()