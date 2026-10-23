from django import forms
from django.core.exceptions import ValidationError

from pessoas.models import Contato, Pessoa


class LoginForm(forms.Form):
    login = forms.CharField(label='Login', max_length=100)
    senha = forms.CharField(label='Senha')


class CadastroForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'exemplo@insa.gov.br',
            }
        )
    )
    telefone = forms.CharField(
        max_length=11,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}
        ),
    )

    class Meta:
        model = Pessoa
        fields = ('nome', 'cpf', 'data_nascimento', 'sexo')

        # Define a aparência dos campos
        widgets = {
            'nome': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Digite o nome completo',
                }
            ),
            'cpf': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Somente números',
                    'maxlength': '11',
                }
            ),
            'data_nascimento': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
        }


    @staticmethod
    def _verifica_digitos_telefone(telefone):
        if not telefone.isnumeric():
            raise ValidationError('O número não é válido.')

    @staticmethod
    def _verifica_existencia_telefone(telefone):
        if Contato.objects.filter(telefone=telefone).exists():
            raise ValidationError('Número de Telefone já cadastrado.')

    def clean_telefone(self):
        telefone_digitado = self.cleaned_data.get('telefone').replace(' ', '')
        self._verifica_digitos_telefone(telefone_digitado)
        self._verifica_existencia_telefone(telefone_digitado)
        return telefone_digitado

    @staticmethod
    def _verifica_padrao_email(email):
        if not email.endswith('@insa.gov.br'):
            raise ValidationError('Este domínio não é permitido.')

    @staticmethod
    def _verifica_existencia_email(email):
        if Contato.objects.filter(email__iexact=email).exists():
            # Não faz diferença de minusculas e maiusculas
            raise ValidationError('E-mail já cadastrado.')

    def clean_email(self):
        email_digitado = self.cleaned_data.get('email').strip().lower()
        self._verifica_padrao_email(email_digitado)
        self._verifica_existencia_email(email_digitado)

        return email_digitado
