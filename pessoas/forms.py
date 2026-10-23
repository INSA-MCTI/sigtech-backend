from django import forms

from pessoas.models import Pessoa


class LoginForm(forms.Form):
    login = forms.CharField(label='Login', max_length=100)
    senha = forms.CharField(label='Senha')


class CadastroForm(forms.ModelForm):
    email = forms.EmailField()
    telefone = forms.CharField(max_length=15)

    class Meta:
        model = Pessoa
        fields = ('nome', 'cpf', 'data_nascimento', 'sexo')

        widgets = {
            'nome': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Digite o nome completo'}
            ),
            'cpf': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Somente números',
                       'maxlength': '11'}
            ),
            'data_nascimento': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),
            'sexo': forms.Select(
                attrs={'class': 'form-select'}
            )
        }
