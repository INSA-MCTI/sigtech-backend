from django import forms

from .models import (
    Arquivo,
    Cargo,
    DadoEstatistico,
    Evento,
    NivelAcesso,
    Pessoa,
    PessoaCargo,
    PessoaUnidade,
    Situacao,
    Unidade,
)


class PessoaForm(forms.ModelForm):
    genero = forms.ChoiceField(
        label='Gênero',
        choices=[('', 'Selecione'), ('M', 'M'), ('F', 'F')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    titulacao = forms.ChoiceField(
        label='Titulação',
        choices=[('', 'Selecione')] + [
            (valor, valor) for valor in (
                'Técnico', 'Graduação', 'Especialização', 'Mestrado',
                'Doutorado', 'Pós-doutorado', 'não possui',
            )
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    escolaridade = forms.ChoiceField(
        label='Escolaridade',
        choices=[('', 'Selecione')] + [
            (valor, valor) for valor in (
                'Ensino Fundamental', 'Ensino Médio', 'Ensino Superior',
            )
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    senha = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        ),
        required=False,
    )

    class Meta:
        model = Pessoa
        fields = [
            'login',
            'nome',
            'dt_nascimento',
            'dt_admissao',
            'dt_demissao',
            'matricula',
            'cpf',
            'id_situacao',
            'id_carreira',
            'escolaridade',
            'titulacao',
            'id_responsavel',
            'cep',
            'logradouro',
            'complemento',
            'bairro',
            'cidade',
            'estado',
            'telefone',
            'email',
            'genero',
            'nivel_acesso',
        ]
        widgets = {
            'dt_nascimento': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'dt_admissao': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'dt_demissao': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date', 'class': 'form-control'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Senha declarada fora de Meta.fields não sobrescreve o hash no modelo.
        self.fields['senha'].required = not bool(self.instance.pk)
        for field_name, field in self.fields.items():
            if 'class' not in (field.widget.attrs.get('class', '')):
                field.widget.attrs['class'] = 'form-control'


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = [
            'titulo',
            'descricao',
            'dt_inicio',
            'dt_fim',
            'tipo',
            'pessoa',
            'geral',
        ]
        widgets = {
            'dt_inicio': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'dt_fim': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'descricao': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(
                field.widget, (forms.CheckboxInput,)
            ):
                field.widget.attrs.setdefault('class', 'form-control')


class ArquivoForm(forms.ModelForm):
    class Meta:
        model = Arquivo
        fields = ['pessoa', 'tipo', 'descricao', 'arquivo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')


class DadoEstatisticoForm(forms.ModelForm):
    class Meta:
        model = DadoEstatistico
        fields = [
            'pessoa',
            'categoria',
            'indicador',
            'valor',
            'periodo',
            'observacao',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')


class PessoaCargoForm(forms.ModelForm):
    class Meta:
        model = PessoaCargo
        fields = ['cargo', 'dt_inicio', 'dt_fim', 'atual']
        widgets = {
            'dt_inicio': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'dt_fim': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date', 'class': 'form-control'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault('class', 'form-control')


class PessoaUnidadeForm(forms.ModelForm):
    class Meta:
        model = PessoaUnidade
        fields = ['unidade', 'dt_inicio', 'dt_fim', 'chefia', 'atual']
        widgets = {
            'dt_inicio': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'dt_fim': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date', 'class': 'form-control'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault('class', 'form-control')


class ImportCSVForm(forms.Form):
    arquivo_csv = forms.FileField(
        label='Arquivo CSV',
        widget=forms.FileInput(attrs={'class': 'form-control'}),
    )


class LoginForm(forms.Form):
    login = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Login',
            }
        ),
    )
    senha = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Senha',
            }
        ),
    )
