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
# Exemplo de tabela normativa (incluindo "Total")
percentile_table_bis11 = {
    "Attention": [5, 6, 7, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 11, 12, 12, 13, 13, 14, 16, 18],
    "Cognitive Instability": [3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 10, 12],
    "Motor": [7, 8, 9, 9, 10, 10 , 11, 11, 12, 12, 12, 13, 13, 14, 14, 15, 15, 16, 18, 20, 23],
    "Perseverance": [4, 4, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 10, 12],
    "Cognitive Complexity": [6, 8, 9, 9, 10, 10, 11, 11, 11, 12, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 18],
    "Self-Control": [6, 8, 9, 10, 10, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16, 17, 18, 19, 22],
    "Total": [40, 47, 50, 52, 53, 55, 56, 58, 59, 60, 62, 63, 64, 65, 67, 68, 70, 72, 76, 80, 90]
}

# Percentis disponíveis
percentile_indices_bis11 = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 99, 100]

# Itens que devem ser invertidos (questões BIS‑11)
itens_para_inverter = [
    1, 7, 8, 9, 10, 12, 13, 15, 20, 29, 30
]
# Note que aqui usamos números (1, 7, 8...) para corresponder a question_1, question_7, etc.
# Se no seu app as chaves forem question_1, question_2..., vamos mapear.

# Mapeamento de respostas string → valores
answer_map = {
    "Raramente ou nunca": 1,
    "Às vezes": 2,
    "Frequentemente": 3,
    "Sempre ou quase sempre": 4
}

# Subescalas de 1ª ordem (Patton et al., 1995)
subscale_mapping = {
    "Attention": [5, 9, 11, 20, 28],
    "Cognitive Instability": [6, 24, 26],
    "Motor": [2, 3, 4, 17, 19, 22],
    "Perseverance": [16, 21, 23],
    "Cognitive Complexity": [10, 15, 18, 27, 29],
    "Self-Control": [1, 7, 8, 12, 13, 14, 30]
}

def find_percentile_interval(score, factor, percentile_table, percentile_indices):
    """
    Encontra o intervalo de percentis com base no escore e no fator.
    """
    scores = percentile_table[factor]  # Lista de escores normativos
    matching_percentiles = []

    # Encontra percentis exatos
    for i, value in enumerate(scores):
        if score == value:
            matching_percentiles.append(percentile_indices[i + 1])

    if not matching_percentiles:
        for i, value in enumerate(scores):
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

def automated_correction_bis11(answers):
    """
    Realiza a correção automatizada do BIS‑11, incluindo:
      - Inversão de itens
      - Cálculo de subescalas
      - Cálculo de total
      - Determinação de percentil (inclusive do total)

    Args:
      answers (dict): Respostas do paciente, ex: {"question_1": "Às vezes", ...}

    Returns:
      dict: Relatório com escores e percentis para cada subescala e para o total.
    """

    # 1) Converter respostas para valores numéricos
    numeric_answers = {}
    for key, value in answers.items():
        # key deve ser algo como "question_1", "question_2"...
        # Precisamos extrair o número da questão
        # Ex: se key = "question_9", question_num = 9
        question_num = int(key.split("_")[1])
        base_value = answer_map.get(value, 0)

        # 2) Inverter se for item invertido
        if question_num in itens_para_inverter:
            base_value = 5 - base_value  # 5 - [1..4] → [4..1]

        numeric_answers[question_num] = base_value

    # 3) Somar subescalas
    scores = {}
    for factor, items in subscale_mapping.items():
        scores[factor] = sum(numeric_answers.get(i, 0) for i in items)

    # 4) Somar total
    total_score = sum(numeric_answers.get(i, 0) for i in range(1, 31))
    scores["Total"] = total_score

    # 5) Calcular percentis para cada subescala + total
    report = {}
    for factor in percentile_table_bis11.keys():
        if factor in scores:
            score = scores[factor]
            p_interval = find_percentile_interval(score, factor, percentile_table_bis11, percentile_indices_bis11)
            report[factor] = {"score": score, "percentile": p_interval}

    # Caso prefira armazenar também as subescalas que não estão em 'percentile_table_bis11',
    # você pode adicionar manualmente ou checar se elas não existem
    # ...
    
    return report

if __name__ == "__main__":
    # Exemplo de uso:
    # Simulando um dicionário de respostas do app (30 itens)
    example_answers = {
        "question_1": "Sempre ou quase sempre",
        "question_2": "Às vezes",
        "question_3": "Frequentemente",
        # ...
        # preencha até question_30
        "question_30": "Raramente ou nunca"
    }
    result = automated_correction_bis11(example_answers)
    print(json.dumps(result, indent=2))