# correction_config.py
import json

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
    # Por exemplo, use a função automated_correction_bis11 e depois determine os intervalos.
    # Este exemplo é simplificado.
    scores = automated_correction_bis11(answers)
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
# Exemplo de tabela normativa (incluindo "Total")
# ============================
# Dados Normativos para BIS‑11
# ============================
# Esses dados são fixos e representam os escores normativos para cada subescala e o total.
# Se necessário, você pode armazená-los em um arquivo ou em uma tabela, mas aqui optamos por defini-los diretamente no código.

percentile_table_bis11 = {
    "Attention": [5, 6, 7, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 11, 12, 12, 13, 13, 14, 16, 18],
    "Cognitive Instability": [3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 10, 12],
    "Motor": [7, 8, 9, 9, 10, 10, 11, 11, 12, 12, 12, 13, 13, 14, 14, 15, 15, 16, 18, 20, 23],
    "Perseverance": [4, 4, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 10, 12],
    "Cognitive Complexity": [6, 8, 9, 9, 10, 10, 11, 11, 11, 12, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 18],
    "Self-Control": [6, 8, 9, 10, 10, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16, 17, 18, 19, 22],
    "Total": [40, 47, 50, 52, 53, 55, 56, 58, 59, 60, 62, 63, 64, 65, 67, 68, 70, 72, 76, 80, 90]
}

percentile_indices_bis11 = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 99, 100]

# ============================
# Configuração de Inversão de Itens
# ============================
# Itens que devem ser invertidos (correspondendo ao número da questão)
itens_para_inverter = [1, 7, 8, 9, 10, 12, 13, 15, 20, 29, 30]

# ============================
# Mapeamento de Respostas e Subescalas
# ============================
# Mapeamento para converter respostas em valores numéricos
answer_map = {
    "Raramente ou nunca": 1,
    "Às vezes": 2,
    "Frequentemente": 3,
    "Sempre ou quase sempre": 4
}

# Mapeamento das subescalas (1ª ordem) conforme Patton et al. (1995)
subscale_mapping = {
    "Attention": [5, 9, 11, 20, 28],
    "Cognitive Instability": [6, 24, 26],
    "Motor": [2, 3, 4, 17, 19, 22],
    "Perseverance": [16, 21, 23],
    "Cognitive Complexity": [10, 15, 18, 27, 29],
    "Self-Control": [1, 7, 8, 12, 13, 14, 30]
}

# ============================
# Função para Encontrar Intervalos de Percentis
# ============================
def find_percentile_interval(score, factor, percentile_table, percentile_indices):
    """
    Encontra o intervalo de percentis com base no escore e no fator.

    Args:
        score (int): Escore do paciente.
        factor (str): Nome do fator/subescala.
        percentile_table (dict): Tabela normativa de percentis para a escala.
        percentile_indices (list): Lista de percentis disponíveis.

    Returns:
        str: Intervalo ou percentil correspondente ao escore.
    """
    normative_scores = percentile_table[factor]
    matching_percentiles = []

    # Tenta encontrar um percentil exato
    for i, value in enumerate(normative_scores):
        if score == value:
            matching_percentiles.append(percentile_indices[i + 1])
    
    # Se nenhum percentil exato foi encontrado, procura o intervalo
    if not matching_percentiles:
        for i, value in enumerate(normative_scores):
            if score <= value:
                if i + 1 < len(percentile_indices):
                    return f"{percentile_indices[i]}-{percentile_indices[i+1]}"
                else:
                    return f"{percentile_indices[-1]}"
        return f"{percentile_indices[-1]}"
    
    if len(matching_percentiles) == 1:
        return f"{matching_percentiles[0]}"
    else:
        return f"{min(matching_percentiles)}-{max(matching_percentiles)}"

# ============================
# Função de Correção Automatizada para BIS‑11
# ============================
def automated_correction_bis11(answers):
    """
    Realiza a correção automatizada do BIS‑11, incluindo:
      - Conversão das respostas para valores numéricos (usando answer_map)
      - Inversão de itens (para os itens presentes em itens_para_inverter)
      - Cálculo dos escores para cada subescala, com base em subscale_mapping
      - Cálculo do escore total (soma de todas as respostas)
      - Determinação dos intervalos percentílicos para cada subescala e para o total

    Args:
        answers (dict): Respostas do paciente, por exemplo, {"question_1": "Às vezes", ..., "question_30": "Sempre ou quase sempre"}

    Returns:
        dict: Relatório com escores e intervalos percentílicos para cada subescala e para o total.
    """
    # Converter as respostas e aplicar inversão quando necessário
    numeric_answers = {}
    for key, value in answers.items():
        # Assume que a chave vem no formato "question_N"
        question_num = int(key.split("_")[1])
        base_value = answer_map.get(value, 0)
        if question_num in itens_para_inverter:
            base_value = 5 - base_value  # Inversão: 5 - [1..4] gera [4..1]
        numeric_answers[question_num] = base_value

    # Calcular escores para cada subescala
    scores = {}
    for factor, items in subscale_mapping.items():
        scores[factor] = sum(numeric_answers.get(i, 0) for i in items)

    # Calcular o escore total (para 30 itens)
    total_score = sum(numeric_answers.get(i, 0) for i in range(1, 31))
    scores["Total"] = total_score

    # Calcular percentis para cada subescala e total usando os dados normativos
    report = {}
    for factor in percentile_table_bis11.keys():
        if factor in scores:
            score = scores[factor]
            p_interval = find_percentile_interval(score, factor, percentile_table_bis11, percentile_indices_bis11)
            report[factor] = {"score": score, "percentile": p_interval}
    
    return report
