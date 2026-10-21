from collections import Counter

from .models import Pessoa, PessoaCargo, PessoaUnidade


def anos_completos(inicio, referencia):
    if inicio is None or inicio > referencia:
        return None
    return referencia.year - inicio.year - (
        (referencia.month, referencia.day) < (inicio.month, inicio.day)
    )


def distribuicao(valores):
    contagens = Counter(
        str(valor).strip() if valor and str(valor).strip()
        else 'Não informado'
        for valor in valores
    )
    return [
        {'rotulo': rotulo, 'total': total}
        for rotulo, total in sorted(contagens.items())
    ]


def tabela_faixas(registros, campo, referencia, faixas):
    linhas = [
        dict(rotulo=rotulo, masculino=0, feminino=0, outros=0, total=0)
        for rotulo, _ in faixas
    ]
    linhas.append(dict(
        rotulo='Não informado / data inválida',
        masculino=0, feminino=0, outros=0, total=0,
    ))
    idades = []
    for pessoa in registros:
        anos = anos_completos(pessoa[campo], referencia)
        if anos is not None:
            idades.append(anos)
        indice = len(faixas)
        if anos is not None:
            indice = next(
                i for i, (_, limite) in enumerate(faixas)
                if limite is None or anos <= limite
            )
        genero = (pessoa['genero'] or '').strip().upper()
        coluna = {'M': 'masculino', 'F': 'feminino'}.get(genero, 'outros')
        linhas[indice][coluna] += 1
        linhas[indice]['total'] += 1
    total = len(registros)
    acumulado = 0
    totais_genero = {
        genero: sum(linha[genero] for linha in linhas)
        for genero in ('masculino', 'feminino')
    }
    acumulados_genero = dict(masculino=0, feminino=0)
    for linha in linhas:
        acumulado += linha['total']
        linha['percentual'] = linha['total'] * 100 / total if total else 0
        linha['acumulado'] = acumulado
        linha['percentual_acumulado'] = (
            acumulado * 100 / total if total else 0
        )
        linha['generos'] = []
        for genero in ('masculino', 'feminino'):
            quantidade = linha[genero]
            acumulados_genero[genero] += quantidade
            subtotal = totais_genero[genero]
            linha['generos'].append({
                'quantidade': quantidade,
                'percentual': quantidade * 100 / subtotal if subtotal else 0,
                'percentual_geral': quantidade * 100 / total if total else 0,
                'acumulado': acumulados_genero[genero],
                'percentual_acumulado': (
                    acumulados_genero[genero] * 100 / subtotal
                    if subtotal else 0
                ),
            })
    return linhas, sum(idades) / len(idades) if idades else None


def relatorio_pessoal(referencia):
    pessoas = Pessoa.objects.filter(deletado=False)
    registros = list(pessoas.values(
        'id', 'genero', 'dt_nascimento', 'dt_admissao', 'titulacao',
        'escolaridade', 'id_situacao__descricao', 'id_carreira__descricao',
    ))
    # A data altera idade e tempo de serviço, não reconstrói o quadro histórico.
    cargos = dict(PessoaCargo.objects.filter(
        pessoa__deletado=False, deletado=False, atual=True,
        cargo__deletado=False,
    ).values_list('pessoa_id', 'cargo__descricao'))
    niveis = dict(PessoaCargo.objects.filter(
        pessoa__deletado=False, deletado=False, atual=True,
        cargo__deletado=False,
    ).values_list('pessoa_id', 'cargo__nivel'))
    unidades = dict(PessoaUnidade.objects.filter(
        pessoa__deletado=False, deletado=False, atual=True,
        unidade__deletado=False,
    ).values_list('pessoa_id', 'unidade__sigla'))
    grupos = [
        ('Situação', [p['id_situacao__descricao'] for p in registros]),
        ('Titulação', [p['titulacao'] for p in registros]),
        ('Escolaridade', [p['escolaridade'] for p in registros]),
        ('Cargo', [cargos.get(p['id']) for p in registros]),
        ('Carreira', [p['id_carreira__descricao'] for p in registros]),
        ('Nível do cargo', [niveis.get(p['id']) for p in registros]),
        ('Unidade', [unidades.get(p['id']) for p in registros]),
    ]
    etarias, media = tabela_faixas(
        registros, 'dt_nascimento', referencia,
        [('Até 30', 30), ('31 a 40', 40), ('41 a 50', 50),
         ('51 a 60', 60), ('Acima de 60', None)],
    )
    servico, _ = tabela_faixas(
        registros, 'dt_admissao', referencia,
        [('0 a 10', 10), ('11 a 20', 20), ('21 a 30', 30),
         ('31 a 40', 40), ('Acima de 40', None)],
    )
    return {
        'total_pessoal': len(registros),
        'grupos': [
            {'titulo': titulo, 'linhas': distribuicao(valores)}
            for titulo, valores in grupos
        ],
        'faixas_etarias': etarias,
        'tempo_servico': servico,
        'idade_media': media,
        'referencia': referencia,
    }
