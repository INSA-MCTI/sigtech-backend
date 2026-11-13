from django.apps import AppConfig


class PessoasConfig(AppConfig):
    name = 'pessoas'
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        import pessoas.signals # Inicia os sinais quando o django inicia