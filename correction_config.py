# correction_config.py

def automated_correction_bis11(answers, normative_table, percentile_indices):
    """
    Realiza a correção automatizada do BIS‑11 com base nas respostas.

    Args:
        answers (dict): Respostas do paciente.
        normative_table (dict): Tabela normativa para o BIS‑11.
        percentile_indices (list): Lista de percentis.

    Returns:
        dict: Relatório de correção com escores e intervalos percentílicos.
    """
    # (Insira aqui a lógica de correção do BIS-11, semelhante ao que já vimos.)
    # Por exemplo, use a função calculate_bis11_scores e depois determine os intervalos.
    # Este exemplo é simplificado.
    scores = calculate_bis11_scores(answers)
    report = {}
    for factor, norms in normative_table.items():
        score = scores.get(factor, 0)
        interval = None
        for i, norm_score in enumerate(norms):
            if score <= norm_score:
                if i + 1 < len(percentile_indices):
                    interval = f"{percentile_indices[i]}-{percentile_indices[i+1]}"
                else:
                    interval = f"{percentile_indices[-1]}"
                break
        if interval is None:
            interval = f"{percentile_indices[-1]}"
        report[factor] = {'score': score, 'percentile': interval}
    report['Total'] = {'score': scores['Total'], 'percentile': None}
    return report

def automated_correction_other_scale(answers, normative_table, percentile_indices):
    """
    Realiza a correção para outra escala (exemplo genérico).
    Essa função deve ser adaptada conforme a estrutura e os dados normativos da escala em questão.

    Args:
        answers (dict): Respostas do paciente.
        normative_table (dict): Tabela normativa para essa escala.
        percentile_indices (list): Lista de percentis.

    Returns:
        dict: Relatório de correção.
    """
    # Exemplo simplificado: apenas soma as respostas.
    total_score = sum(int(value) for value in answers.values())
    return {'Total': {'score': total_score, 'percentile': None}}

# Dados normativos para BIS‑11 (exemplo)
normative_table_bis11 = {
    'Attention': [5, 6, 7, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 11, 12, 12, 13, 13, 14, 16, 18],
    'Cognitive Instability': [3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 10, 12],
    'Motor Impulsiveness': [7, 8, 9, 9, 10, 10, 11, 11, 12, 12, 12, 13, 13, 14, 14, 15, 15, 16, 18, 20, 23],
    'Perseverance': [4, 4, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 10, 12],
    'Cognitive Complexity': [6, 8, 9, 9, 10, 10, 11, 11, 11, 12, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 18],
    'Self-Control': [6, 8, 9, 10, 10, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16, 17, 18, 19, 22]
}
percentile_indices_bis11 = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 99, 100]

# Configuração de correção para cada escala
correction_config = {
    'BIS-11': {
        'normative_table': normative_table_bis11,
        'percentile_indices': percentile_indices_bis11,
        'correction_function': automated_correction_bis11
    },
    'OutraEscala': {
        # Configure os dados normativos e função de correção para essa escala, se houver.
        'normative_table': {},  # Exemplo vazio
        'percentile_indices': [],
        'correction_function': automated_correction_other_scale
    }
}

# Exemplo de função auxiliar para calcular BIS-11 (você pode colocar a lógica real aqui)
def calculate_bis11_scores(answers):
    # Lógica simplificada: suponha que cada resposta numérica seja extraída do mapeamento
    answer_map = {
        'Raramente ou nunca': 1,
        'Às vezes': 2,
        'Frequentemente': 3,
        'Sempre ou quase sempre': 4
    }
    scores = {}
    # Divida os 30 itens em subescalas conforme o mapeamento (exemplo simplificado)
    subscale_mapping = {
        'Attention': [5, 9, 11, 20, 28],
        'Cognitive Instability': [6, 24, 26],
        'Motor Impulsiveness': [2, 3, 4, 17, 19, 22],
        'Perseverance': [16, 21, 23],
        'Cognitive Complexity': [10, 15, 18, 27, 29],
        'Self-Control': [1, 7, 8, 12, 13, 14, 30]
    }
    for factor, items in subscale_mapping.items():
        scores[factor] = sum(answer_map.get(answers.get(f'question_{i}', ''), 0) for i in items)
    total = sum(answer_map.get(answers.get(f'question_{i}', ''), 0) for i in range(1, 31))
    scores['Total'] = total
    return scores
